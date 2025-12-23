"""
File: app/llm.py
Description: GPT-4.1-mini wrapper for a Bangla chatbot that generates answers using provided context.
"""

import os  # Import the OS module to access environment variables
from dotenv import load_dotenv  # Import load_dotenv to load environment variables from a .env file
from openai import OpenAI  # Import OpenAI class to interact with OpenAI API

load_dotenv()  # Load environment variables from a .env file into the environment

class BanglaLLM:
    """
    A wrapper class for interacting with GPT-4.1-mini model for Bangla question answering.
    """

    def __init__(self):
        # Initialize the OpenAI client with API key and custom base URL
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),  # Fetch API key from environment variables
            base_url="https://models.inference.ai.azure.com"  # Set the Azure OpenAI base URL
        )

    def generate_answer(self, question: str, context: str) -> str:
        """
        Generate an answer in Bangla given a question and context.
        """

        # Construct the prompt that instructs the model to answer using provided context
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

        # Call the OpenAI chat completion API with GPT-4.1-mini model
        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",  # Specify the GPT-4.1-mini model
            messages=[{"role": "user", "content": prompt}],  # Pass the prompt as user message
            temperature=0.3  # Set temperature for controlled randomness
        )

        # Return the model's response text after stripping extra spaces
        return response.choices[0].message.content.strip()
