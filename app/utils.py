"""
File: utils.py
Directory: app/utils.py
Description: 
This file contains utility functions for text processing and analysis. 
It includes text normalization, intent detection using FAQ JSON data, 
sentiment analysis with NLTK, and datetime normalization.
"""

# Import regular expression module for text processing
import re
# Import JSON module to load FAQ data
import json
# Import sentiment analyzer from NLTK
from nltk.sentiment import SentimentIntensityAnalyzer
# Import datetime and timezone utilities
from datetime import datetime, timezone

# Load FAQ data from JSON file located at app/faq_data.json with UTF-8-sig encoding
with open("app/faq_data.json", encoding="utf-8-sig") as f:
    FAQ_DATA = json.load(f)

# Initialize NLTK's sentiment intensity analyzer
sia = SentimentIntensityAnalyzer()


# Function to normalize text: lowercase and remove non-alphanumeric characters
def normalize_text(text: str) -> str:
    # Convert text to lowercase
    text = text.lower()
    # Remove all characters except word characters and whitespace
    text = re.sub(r"[^\w\s]", "", text)
    # Return the normalized text
    return text


# Function to detect intent from input text using keywords in FAQ data
def detect_intent(text: str):
    # Iterate over each FAQ record
    for record in FAQ_DATA:
        # Iterate over each keyword in the record
        for kw in record["keywords"]:
            # If the keyword exists in input text (case-insensitive)
            if kw.lower() in text:
                # Return the matching record
                return record
    # Return None if no intent matched
    return None


# Function to analyze sentiment of input text
def sentiment_analysis(text: str) -> str:
    # Get polarity scores from sentiment intensity analyzer
    score = sia.polarity_scores(text)
    # Determine sentiment based on compound score
    if score["compound"] >= 0.05:
        return "positive"  # Positive sentiment
    elif score["compound"] <= -0.05:
        return "negative"  # Negative sentiment
    return "neutral"  # Neutral sentiment


# Function to normalize datetime objects or strings to UTC-aware datetime
def normalize_datetime(dt):
    # If input is a string
    if isinstance(dt, str):
        try:
            # Convert ISO format string to datetime object
            dt = datetime.fromisoformat(dt)
        except Exception:
            # If conversion fails, return current UTC datetime
            return datetime.now(timezone.utc)

    # If input is already a datetime object
    if isinstance(dt, datetime):
        # If datetime object is naive (no timezone), set UTC
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        # Return datetime if timezone-aware
        return dt

    # If input is neither string nor datetime, return current UTC datetime
    return datetime.now(timezone.utc)
