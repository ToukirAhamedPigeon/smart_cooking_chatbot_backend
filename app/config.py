"""
File: config.py
Directory: app/config.py

Summary:
This file loads environment variables and serves as the central configuration 
module for the entire project, providing settings like MongoDB URI, Redis URL, 
and cache TTL.
"""

import os  # Import the built-in os module to interact with environment variables
from dotenv import load_dotenv  # Import load_dotenv to load environment variables from a .env file

# Load environment variables from a .env file located at the project root
load_dotenv()

# MongoDB URI: Get the value from the environment variable "MONGO_URI", fallback to "mongodb://localhost:27017" if not set
MONGO_URI = os.getenv("MONGO_URI") or "mongodb://localhost:27017"

# Redis URL: Get the value from the environment variable "REDIS_URL", fallback to "redis://localhost:6379/0" if not set
REDIS_URL = os.getenv("REDIS_URL") or "redis://localhost:6379/0"

# Cache TTL (Time-To-Live) in seconds for Redis entries
REDIS_TTL = 3600
