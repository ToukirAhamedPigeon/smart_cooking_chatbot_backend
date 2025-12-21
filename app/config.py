"""
config.py

এই ফাইলটি environment variables load করে
এবং পুরো প্রজেক্টে central configuration হিসেবে কাজ করে
"""

import os
from dotenv import load_dotenv

# .env লোড করা
load_dotenv()

# MongoDB URI
MONGO_URI = os.getenv("MONGO_URI") or "mongodb://localhost:27017"

# Redis URL
REDIS_URL = os.getenv("REDIS_URL") or "redis://localhost:6379/0"

# Cache TTL (seconds)
REDIS_TTL = 3600
