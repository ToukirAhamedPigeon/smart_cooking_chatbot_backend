"""
db.py

MongoDB Atlas connection
- users
- chat_histories
"""

from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)

db = client.smart_cooking_db

users_collection = db.users
chat_collection = db.chat_histories
