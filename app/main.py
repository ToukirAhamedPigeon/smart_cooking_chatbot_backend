from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import UserMessage, ChatResponse, UserRegister, ChatHistoryResponse
from app.chatbot import get_reply
from app.db import users_collection
from datetime import datetime, timezone
from app.services.history_service import load_chat_history

app = FastAPI(title="Smart Cooking Customer Support Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# User registration
@app.post("/register")
async def register(user: UserRegister):
    try:
        doc = {"mobile": user.mobile, "name": user.name or "", "created_at": datetime.now(timezone.utc)}
        result = await users_collection.update_one({"mobile": user.mobile}, {"$setOnInsert": doc}, upsert=True)
        user_id = user.mobile
        return {"user_id": user_id, "message": "User registered successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(user_msg: UserMessage):
    try:
        return await get_reply(user_msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/history/{user_id}", response_model=ChatHistoryResponse)
async def get_chat_history(user_id: str):
    try:
        return await load_chat_history(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

