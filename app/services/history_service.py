# history_service.py
from app.redis_client import r
from app.db import chat_collection
from app.models import ChatHistoryResponse
from app.config import REDIS_TTL
import json
from datetime import datetime

async def load_chat_history(user_id: str) -> ChatHistoryResponse:
    redis_key = f"chat_history:{user_id}"

    cached = r.get(redis_key)
    if cached:
        return ChatHistoryResponse(
            user_id=user_id,
            messages=json.loads(cached),  # <-- here
            source="redis"
        )

    doc = await chat_collection.find_one({"user_id": user_id})
    messages = doc.get("messages", []) if doc else []

    # sort by created_at
    messages = sorted(messages, key=lambda x: x.get("created_at"))

    # Provide default created_at if missing
    for msg in messages:
        if "created_at" not in msg or not msg["created_at"]:
            msg["created_at"] = datetime.now()  # <-- datetime used here

    r.setex(redis_key, REDIS_TTL, json.dumps(messages, default=str))

    return ChatHistoryResponse(
        user_id=user_id,
        messages=messages,
        source="mongodb"
    )
