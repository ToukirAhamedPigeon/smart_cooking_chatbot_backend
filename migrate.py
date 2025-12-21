"""
migrate.py

MongoDB collections initialization for Smart Cooking Chatbot.

- Creates 'users' collection with indexes
- Creates 'chat_histories' collection with indexes
"""

from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI") or "mongodb://localhost:27017"
DB_NAME = "smart_cooking_db"

async def migrate():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]

    # Users collection
    users = db.users
    await users.create_index("mobile", unique=True)
    print("✅ 'users' collection ready with unique index on 'mobile'")

    # Chat Histories collection
    chats = db.chat_histories
    await chats.create_index("user_id")
    print("✅ 'chat_histories' collection ready with index on 'user_id'")

    # Close client (synchronous)
    client.close()
    print("MongoDB connection closed.")

if __name__ == "__main__":
    asyncio.run(migrate())
