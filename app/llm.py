"""
llm.py

- GPT-4.1-mini wrapper for Bangla chatbot
- Generates answer using context
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class BanglaLLM:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://models.inference.ai.azure.com"
        )

    def generate_answer(self, question: str, context: str) -> str:
        prompt = f"""
তুমি একজন বাংলা সহকারী।
শুধুমাত্র নিচের তথ্য ব্যবহার করে উত্তর দাও।
যদি তথ্য না পাওয়া যায়, বলো: "এই বিষয়ে আমার কাছে তথ্য নেই।"

তথ্য:
{context}

প্রশ্ন:
{question}

উত্তর বাংলা ভাষায় দাও।
"""
        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
