"""
redis_client.py

Redis usage:
- FAQ cache
- User short-term context
"""

import redis
from app.config import REDIS_URL

r = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True
)
