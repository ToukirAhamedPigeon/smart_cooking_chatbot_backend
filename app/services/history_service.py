# File: app/services/history_service.py
# Summary:
# This service module provides functionality to load a user's chat history.
# It first attempts to retrieve the history from Redis cache for faster access.
# If the data is not in Redis, it fetches it from MongoDB, normalizes timestamps,
# sorts the messages, caches the result in Redis, and then returns the data.

from app.redis_client import r  # Import the Redis client instance
from app.db import chat_collection  # Import the MongoDB collection for chats
from app.models import ChatHistoryResponse  # Import the response model for chat history
from app.config import REDIS_TTL  # Import the Redis time-to-live setting
from app.utils import normalize_datetime  # Import utility to normalize datetime fields
import json  # Import JSON module for serialization/deserialization

async def load_chat_history(user_id: str) -> ChatHistoryResponse:
    # Define a Redis key for storing/fetching the user's chat history
    redis_key = f"chat_history:{user_id}"

    # 1️⃣ Attempt to retrieve cached messages from Redis
    cached = r.get(redis_key)
    if cached:
        # Deserialize the cached JSON string into Python objects
        messages = json.loads(cached)

        # Normalize the 'created_at' field of each message
        for msg in messages:
            msg["created_at"] = normalize_datetime(msg.get("created_at"))

        # Return the chat history with a flag indicating it came from Redis
        return ChatHistoryResponse(
            user_id=user_id,
            messages=messages,
            source="redis"
        )

    # 2️⃣ If not in Redis, fetch the user's chat document from MongoDB
    doc = await chat_collection.find_one({"user_id": user_id})
    # Extract the 'messages' list from the document or use an empty list
    messages = doc.get("messages", []) if doc else []

    # Normalize the 'created_at' field of each message
    for msg in messages:
        msg["created_at"] = normalize_datetime(msg.get("created_at"))

    # Sort the messages chronologically by 'created_at'
    messages = sorted(messages, key=lambda x: x["created_at"])

    # 3️⃣ Save the sorted messages into Redis with a TTL
    r.setex(redis_key, REDIS_TTL, json.dumps(messages, default=str))

    # Return the chat history with a flag indicating it came from MongoDB
    return ChatHistoryResponse(
        user_id=user_id,
        messages=messages,
        source="mongodb"
    )
