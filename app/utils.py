"""
utils.py

- Normalize text
- Intent detection from JSON
- Sentiment analysis
"""

import re
import json
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime, timezone

with open("app/faq_data.json", encoding="utf-8-sig") as f:
    FAQ_DATA = json.load(f)

sia = SentimentIntensityAnalyzer()


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text


def detect_intent(text: str):
    for record in FAQ_DATA:
        for kw in record["keywords"]:
            if kw.lower() in text:
                return record
    return None


def sentiment_analysis(text: str) -> str:
    score = sia.polarity_scores(text)
    if score["compound"] >= 0.05:
        return "positive"
    elif score["compound"] <= -0.05:
        return "negative"
    return "neutral"

def normalize_datetime(dt):
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except Exception:
            return datetime.now(timezone.utc)

    if isinstance(dt, datetime):
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt

    return datetime.now(timezone.utc)
