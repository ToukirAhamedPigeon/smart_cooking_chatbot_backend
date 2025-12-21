# check_redis.py
# এই ফাইলটি Redis server এ connection ঠিক আছে কিনা পরীক্ষা করে

import redis
import os
from dotenv import load_dotenv
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

print("REDIS_URL =", os.getenv("REDIS_URL"))
print("MONGO_URI =", os.getenv("MONGO_URI"))

load_dotenv()  # .env থেকে environment variable load করবে

REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    raise ValueError("REDIS_URL environment variable is not set.")

# Redis client create
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

try:
    # PING দিয়ে connection check
    response = r.ping()
    if response:
        print("✅ Redis connection successful!")
    else:
        print("❌ Redis connection failed.")
except Exception as e:
    print("❌ Redis connection error:", e)
