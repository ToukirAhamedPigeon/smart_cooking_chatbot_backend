"""
chatbot.py

- Redis cache
- FAQ lookup
- MongoDB chat history
- Context-aware LLM response
"""

from app.utils import normalize_text, detect_intent, sentiment_analysis
from app.redis_client import r
from app.db import chat_collection, users_collection
from app.models import UserMessage, ChatResponse
from app.config import REDIS_TTL
from app.llm import BanglaLLM

llm = BanglaLLM()

async def get_reply(user_msg: UserMessage) -> ChatResponse:
    normalized = normalize_text(user_msg.message)
    sentiment = sentiment_analysis(user_msg.message)
    cache_key = f"{user_msg.user_id}:{normalized}"

    # 1️⃣ Redis cache check
    cached = r.get(cache_key)
    if cached:
        return ChatResponse(reply=cached, source="redis-cache", sentiment=sentiment)

    # 2️⃣ FAQ lookup
    record = detect_intent(normalized)
    if record:
        reply = record["answer_en"]  # default English, you can localize if needed
        source = "json"
        r.setex(cache_key, REDIS_TTL, reply)
    else:
        # 3️⃣ Retrieve previous user messages from MongoDB for context
        history_doc = await chat_collection.find_one({"user_id": user_msg.user_id})
        context = ""
        if history_doc:
            context = "\n".join([f"User: {m['message']} | Reply: {m['reply']}" for m in history_doc.get("messages", [])])

        # 4️⃣ Generate reply via LLM
        reply = llm.generate_answer(user_msg.message, context)
        source = "llm"

        r.setex(cache_key, REDIS_TTL, reply)

    # 5️⃣ Save chat to MongoDB
    await chat_collection.update_one(
        {"user_id": user_msg.user_id},
        {"$push": {"messages": {"message": user_msg.message, "reply": reply, "sentiment": sentiment}}},
        upsert=True
    )

    return ChatResponse(reply=reply, source=source, sentiment=sentiment)
