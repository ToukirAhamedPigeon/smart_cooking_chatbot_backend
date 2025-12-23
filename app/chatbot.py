# File: app/chatbot.py
# Description: This module handles processing of user messages for the Bangla chatbot.
# It normalizes user input, checks Redis cache for previous responses, searches FAQ data,
# retrieves chat history from MongoDB for context, queries the Bangla LLM for an answer,
# caches the response, stores chat history, and returns a structured ChatResponse including
# sentiment and source information.

from datetime import datetime, timezone  # Import datetime utilities for timestamping messages
from app.utils import normalize_text, detect_intent, sentiment_analysis, FAQ_DATA  # Import utility functions and FAQ data
from app.redis_client import r  # Import Redis client instance
from app.db import chat_collection  # Import MongoDB collection for chat messages
from app.models import UserMessage, ChatResponse  # Import data models for user messages and chatbot responses
from app.config import REDIS_TTL  # Import Redis TTL configuration
from app.llm import BanglaLLM  # Import Bangla language model class

llm = BanglaLLM()  # Initialize the Bangla language model instance

async def get_reply(user_msg: UserMessage) -> ChatResponse:
    normalized = normalize_text(user_msg.message)  # Normalize the user's message text
    sentiment = sentiment_analysis(user_msg.message)  # Analyze the sentiment of the user's message
    cache_key = f"{user_msg.user_id}:{normalized}"  # Create a unique cache key for Redis

    # 1️⃣ Redis cache
    cached = r.get(cache_key)  # Check if the response exists in Redis cache
    if cached:
        return ChatResponse(
            reply=cached,  # Return the cached reply
            source="redis-cache",  # Indicate the response came from Redis cache
            sentiment=sentiment  # Include the sentiment analysis
        )

    # 2️⃣ FAQ lookup
    record = detect_intent(normalized)  # Check if the normalized message matches any FAQ intent
    if record:
        reply = record["answer_bn"]  # Get the answer in Bangla from the FAQ
        source = "json"  # Mark the source as JSON (FAQ)
        r.setex(cache_key, REDIS_TTL, reply)  # Store the reply in Redis with TTL
    else:
        # 3️⃣ Chat history for context
        history_doc = await chat_collection.find_one({"user_id": user_msg.user_id})  # Retrieve user's chat history from MongoDB
        context_history = ""  # Initialize context history string
        if history_doc:
            context_history = "\n".join(
                [f"User: {m['message']} | Reply: {m['reply']}"
                 for m in history_doc.get("messages", [])]  # Format previous messages and replies
            )

        # 4️⃣ FAQ context
        faq_context = "\n".join(
            [f"{f['topic']}: {f['answer_bn']}" for f in FAQ_DATA]  # Concatenate all FAQ topics and answers
        )

        # Combine FAQ context and chat history for LLM input
        context = f"""
FAQ তথ্য:
{faq_context}

চ্যাট ইতিহাস:
{context_history}
        """

        # 5️⃣ LLM
        reply = llm.generate_answer(user_msg.message, context)  # Generate a reply using Bangla LLM with context
        source = "llm"  # Mark the source as LLM
        r.setex(cache_key, REDIS_TTL, reply)  # Cache the LLM response in Redis

    # 6️⃣ Save to MongoDB
    await chat_collection.update_one(
        {"user_id": user_msg.user_id},  # Filter for the specific user
        {
            "$push": {
                "messages": {
                    "message": user_msg.message,  # Store the original user message
                    "reply": reply,  # Store the generated reply
                    "sentiment": sentiment,  # Store sentiment analysis
                    "created_at": datetime.now(timezone.utc)  # Timestamp in UTC
                }
            }
        },
        upsert=True  # Create a new document if it does not exist
    )

    # 7️⃣ Invalidate history cache
    r.delete(f"chat_history:{user_msg.user_id}")  # Delete cached chat history to maintain consistency

    return ChatResponse(
        reply=reply,  # Return the final reply
        source=source,  # Return the source of the reply (FAQ, LLM, or Redis)
        sentiment=sentiment  # Return the sentiment of the message
    )
