"""
File: llm.py
Directory: app/

Summary:
This file defines the FastAPI application for the Smart Cooking Customer Support Chatbot. 
It handles user registration, chat message processing, and retrieving chat history.
The application includes CORS middleware to allow cross-origin requests and integrates with
MongoDB for user data and chat history. Chat responses are generated via the `get_reply` function
from the chatbot module.
"""

from fastapi import FastAPI, HTTPException  # Import FastAPI framework and HTTPException for error handling
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware to handle cross-origin requests
from app.models import UserMessage, ChatResponse, UserRegister, ChatHistoryResponse  # Import Pydantic models
from app.chatbot import get_reply  # Import chatbot function to generate replies
from app.db import users_collection  # Import MongoDB users collection
from datetime import datetime, timezone  # Import datetime and timezone utilities
from app.services.history_service import load_chat_history  # Import function to load chat history from DB

# Initialize FastAPI app with title
app = FastAPI(title="Smart Cooking Customer Support Chatbot")

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"]   # Allow all headers
)

# User registration endpoint
@app.post("/register")
async def register(user: UserRegister):
    try:
        # Create a document with mobile, name, and current UTC time
        doc = {"mobile": user.mobile, "name": user.name or "", "created_at": datetime.now(timezone.utc)}
        # Insert the document if mobile does not exist, otherwise do nothing
        result = await users_collection.update_one({"mobile": user.mobile}, {"$setOnInsert": doc}, upsert=True)
        # Use mobile as user ID
        user_id = user.mobile
        # Return success message and user_id
        return {"user_id": user_id, "message": "User registered successfully."}
    except Exception as e:
        # Raise HTTP 500 error if any exception occurs
        raise HTTPException(status_code=500, detail=str(e))

# Chat endpoint to handle user messages
@app.post("/chat", response_model=ChatResponse)
async def chat(user_msg: UserMessage):
    try:
        # Call chatbot function to get response for user message
        return await get_reply(user_msg)
    except Exception as e:
        # Raise HTTP 500 error if any exception occurs
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to retrieve chat history for a user
@app.get("/chat/history/{user_id}", response_model=ChatHistoryResponse)
async def get_chat_history(user_id: str):
    try:
        # Load chat history from database
        return await load_chat_history(user_id)
    except Exception as e:
        # Raise HTTP 500 error if any exception occurs
        raise HTTPException(status_code=500, detail=str(e))
