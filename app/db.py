"""
File: app/db.py
Description: This file establishes the MongoDB Atlas connection using Motor (async MongoDB driver).
It defines references to the 'users' and 'chat_histories' collections for use across the app.
"""

# Import the asynchronous MongoDB client from the Motor library
from motor.motor_asyncio import AsyncIOMotorClient

# Import the MongoDB connection URI from the app's configuration file
from app.config import MONGO_URI

# Create an asynchronous MongoDB client using the connection URI
client = AsyncIOMotorClient(MONGO_URI)

# Access the 'smart_cooking_db' database from the MongoDB client
db = client.smart_cooking_db

# Define a reference to the 'users' collection within the database
users_collection = db.users

# Define a reference to the 'chat_histories' collection within the database
chat_collection = db.chat_histories
