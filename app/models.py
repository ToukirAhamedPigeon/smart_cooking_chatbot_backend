from pydantic import BaseModel
from typing import Optional, List

# User registration request
class UserRegister(BaseModel):
    mobile: str  # user mobile number
    name: Optional[str] = None

# User message request
class UserMessage(BaseModel):
    user_id: str  # MongoDB ObjectId or mobile
    message: str

# Chat response with source and sentiment
class ChatResponse(BaseModel):
    reply: str
    source: str
    sentiment: Optional[str] = None

# Chat history
class ChatHistory(BaseModel):
    user_id: str
    messages: List[dict]
