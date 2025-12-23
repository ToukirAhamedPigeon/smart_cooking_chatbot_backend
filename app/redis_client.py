"""
File: redis_client.py
Directory: app/llm.py
Summary:
This file sets up the Redis client for the application. 
It is used for caching FAQs and storing user short-term context.
"""

# Import the Redis library to interact with Redis database
import redis

# Import the Redis connection URL from the application's config
from app.config import REDIS_URL

# Create a Redis client instance using the connection URL
# decode_responses=True ensures that Redis responses are returned as Python strings
r = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True
)
