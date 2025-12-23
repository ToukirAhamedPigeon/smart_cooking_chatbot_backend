# app/services/history_service.py
from app.redis_client import r
from app.db import chat_collection
from app.models import ChatHistoryResponse
from app.config import REDIS_TTL
from app.utils import normalize_datetime
import json

async def load_chat_history(user_id: str) -> ChatHistoryResponse:
    redis_key = f"chat_history:{user_id}"

    # 1️⃣ Redis
    cached = r.get(redis_key)
    if cached:
        messages = json.loads(cached)

        for msg in messages:
            msg["created_at"] = normalize_datetime(msg.get("created_at"))

        return ChatHistoryResponse(
            user_id=user_id,
            messages=messages,
            source="redis"
        )

    # 2️⃣ MongoDB
    doc = await chat_collection.find_one({"user_id": user_id})
    messages = doc.get("messages", []) if doc else []

    for msg in messages:
        msg["created_at"] = normalize_datetime(msg.get("created_at"))

    messages = sorted(messages, key=lambda x: x["created_at"])

    # 3️⃣ Save to Redis
    r.setex(redis_key, REDIS_TTL, json.dumps(messages, default=str))

    return ChatHistoryResponse(
        user_id=user_id,
        messages=messages,
        source="mongodb"
    )
