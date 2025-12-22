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

    # Users
    users = db.users
    await users.create_index("mobile", unique=True)
    print("✅ users.mobile unique index created")

    # Chat histories
    chats = db.chat_histories
    await chats.create_index("user_id")
    await chats.create_index("messages.created_at")
    print("✅ chat_histories indexes created")

    client.close()

if __name__ == "__main__":
    asyncio.run(migrate())
