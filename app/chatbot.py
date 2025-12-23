# app/chatbot.py
from datetime import datetime, timezone
from app.utils import normalize_text, detect_intent, sentiment_analysis, FAQ_DATA
from app.redis_client import r
from app.db import chat_collection
from app.models import UserMessage, ChatResponse
from app.config import REDIS_TTL
from app.llm import BanglaLLM

llm = BanglaLLM()

async def get_reply(user_msg: UserMessage) -> ChatResponse:
    normalized = normalize_text(user_msg.message)
    sentiment = sentiment_analysis(user_msg.message)
    cache_key = f"{user_msg.user_id}:{normalized}"

    # 1️⃣ Redis cache
    cached = r.get(cache_key)
    if cached:
        return ChatResponse(
            reply=cached,
            source="redis-cache",
            sentiment=sentiment
        )

    # 2️⃣ FAQ lookup
    record = detect_intent(normalized)
    if record:
        reply = record["answer_bn"]
        source = "json"
        r.setex(cache_key, REDIS_TTL, reply)
    else:
        # 3️⃣ Chat history for context
        history_doc = await chat_collection.find_one({"user_id": user_msg.user_id})
        context_history = ""
        if history_doc:
            context_history = "\n".join(
                [f"User: {m['message']} | Reply: {m['reply']}"
                 for m in history_doc.get("messages", [])]
            )

        # 4️⃣ FAQ context
        faq_context = "\n".join(
            [f"{f['topic']}: {f['answer_bn']}" for f in FAQ_DATA]
        )

        context = f"""
FAQ তথ্য:
{faq_context}

চ্যাট ইতিহাস:
{context_history}
        """

        # 5️⃣ LLM
        reply = llm.generate_answer(user_msg.message, context)
        source = "llm"
        r.setex(cache_key, REDIS_TTL, reply)

    # 6️⃣ Save to MongoDB
    await chat_collection.update_one(
        {"user_id": user_msg.user_id},
        {
            "$push": {
                "messages": {
                    "message": user_msg.message,
                    "reply": reply,
                    "sentiment": sentiment,
                    "created_at": datetime.now(timezone.utc)
                }
            }
        },
        upsert=True
    )

    # 7️⃣ Invalidate history cache
    r.delete(f"chat_history:{user_msg.user_id}")

    return ChatResponse(
        reply=reply,
        source=source,
        sentiment=sentiment
    )
