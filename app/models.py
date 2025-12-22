from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ---------- User ----------
class UserRegister(BaseModel):
    mobile: str
    name: Optional[str] = None


# ---------- Chat ----------
class UserMessage(BaseModel):
    user_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str
    source: str
    sentiment: Optional[str] = None


# ---------- Chat History ----------
class ChatMessage(BaseModel):
    message: str
    reply: str
    sentiment: Optional[str] = None
    created_at: Optional[datetime] = None

class ChatHistoryResponse(BaseModel):
    user_id: str
    messages: List[ChatMessage]
    source: str
