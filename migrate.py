"""
File: migrate.py
Directory: root (or your project directory)
Description: 
This script connects to a MongoDB database using Motor (AsyncIOMotorClient) and creates necessary indexes 
for the 'users' and 'chat_histories' collections. It ensures that user mobile numbers are unique and 
optimizes queries for chat histories by creating indexes on user_id and messages.created_at.
"""

# Import AsyncIOMotorClient for asynchronous MongoDB operations
from motor.motor_asyncio import AsyncIOMotorClient

# Import asyncio for running asynchronous code
import asyncio

# Import os to access environment variables
import os

# Import load_dotenv to load environment variables from a .env file
from dotenv import load_dotenv

# Load environment variables from .env file into the system environment
load_dotenv()

# Get the MongoDB URI from environment variable, or default to local MongoDB
MONGO_URI = os.getenv("MONGO_URI") or "mongodb://localhost:27017"

# Define the database name to use
DB_NAME = "smart_cooking_db"

# Define an asynchronous function to create indexes (migration)
async def migrate():
    # Create an asynchronous MongoDB client using the given URI
    client = AsyncIOMotorClient(MONGO_URI)

    # Select the database by name
    db = client[DB_NAME]

    # Reference the 'users' collection
    users = db.users

    # Create a unique index on the 'mobile' field of the 'users' collection
    await users.create_index("mobile", unique=True)
    
    # Print a message confirming the unique index creation
    print("✅ users.mobile unique index created")

    # Reference the 'chat_histories' collection
    chats = db.chat_histories

    # Create an index on 'user_id' field of 'chat_histories' collection
    await chats.create_index("user_id")

    # Create an index on 'messages.created_at' field of 'chat_histories' collection
    await chats.create_index("messages.created_at")

    # Print a message confirming the chat_histories indexes creation
    print("✅ chat_histories indexes created")

    # Close the MongoDB client connection
    client.close()

# Run the migrate function if this script is executed directly
if __name__ == "__main__":
    asyncio.run(migrate())
