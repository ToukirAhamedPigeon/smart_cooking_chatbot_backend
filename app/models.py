"""
File: models.py
Directory: app/models.py
Description:
This file contains Pydantic models used for the Smart Cooking Chat application. 
It defines data structures for user registration, sending messages, receiving chat responses,
and retrieving chat history. These models are used for data validation and type checking in the backend.
"""

from pydantic import BaseModel  # Import BaseModel from Pydantic to define data models with type validation
from typing import Optional, List  # Import Optional for optional fields, List for typed lists
from datetime import datetime  # Import datetime to handle timestamp fields


# ---------- User ----------
class UserRegister(BaseModel):
    mobile: str  # Required field for the user's mobile number
    name: Optional[str] = None  # Optional field for the user's name, defaults to None


# ---------- Chat ----------
class UserMessage(BaseModel):
    user_id: str  # ID of the user sending the message
    message: str  # The content of the user's message


class ChatResponse(BaseModel):
    reply: str  # Chatbot's reply text
    source: str  # Source of the reply (e.g., knowledge base or FAQ)
    sentiment: Optional[str] = None  # Optional sentiment of the reply, defaults to None


# ---------- Chat History ----------
class ChatMessage(BaseModel):
    message: str  # The original user message
    reply: str  # The chatbot's reply
    sentiment: Optional[str] = None  # Optional sentiment of the message/reply
    created_at: Optional[datetime] = None  # Optional timestamp of when the message was created


class ChatHistoryResponse(BaseModel):
    user_id: str  # ID of the user whose chat history is being retrieved
    messages: List[ChatMessage]  # List of chat messages exchanged with the user
    source: str  # Source of the chat history (e.g., database, knowledge base)
