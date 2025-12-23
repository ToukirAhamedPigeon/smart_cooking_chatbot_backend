# File: check_redis.py
# Directory: root folder (or wherever this file resides)
# Summary: This script checks whether the Redis server connection is working properly. 
# It loads environment variables from a .env file, retrieves the REDIS_URL, and attempts to ping the Redis server.

import redis  # Import the Redis library to interact with Redis server
import os  # Import os module to access environment variables
from dotenv import load_dotenv  # Import load_dotenv to load .env file variables
from pathlib import Path  # Import Path from pathlib to handle file paths

env_path = Path('.') / '.env'  # Define the path to the .env file in the current directory
load_dotenv(dotenv_path=env_path)  # Load environment variables from the specified .env file

print("REDIS_URL =", os.getenv("REDIS_URL"))  # Print the REDIS_URL from environment variables
print("MONGO_URI =", os.getenv("MONGO_URI"))  # Print the MONGO_URI from environment variables

load_dotenv()  # Load environment variables from default .env file location

REDIS_URL = os.getenv("REDIS_URL")  # Retrieve the REDIS_URL from environment variables
if not REDIS_URL:  # Check if REDIS_URL is not set
    raise ValueError("REDIS_URL environment variable is not set.")  # Raise an error if REDIS_URL is missing

# Redis client create
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)  # Create a Redis client from the URL with response decoding enabled

try:
    # PING দিয়ে connection check
    response = r.ping()  # Send a PING command to Redis to check connection
    if response:  # If ping returns True
        print("✅ Redis connection successful!")  # Print success message
    else:  # If ping returns False
        print("❌ Redis connection failed.")  # Print failure message
except Exception as e:  # Catch any exceptions during the connection check
    print("❌ Redis connection error:", e)  # Print the exception message
