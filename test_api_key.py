"""Test script to verify API key loading"""
import os
from dotenv import load_dotenv

# Load from .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(f"Loaded API Key length: {len(api_key) if api_key else 'None'}")
print(f"First 30 chars: {api_key[:30] if api_key else 'None'}")
print(f"Last 10 chars: {api_key[-10:] if api_key else 'None'}")
print(f"\nFull key:\n{api_key}")
print(f"\nDoes it start with 'sk-proj-'? {api_key.startswith('sk-proj-') if api_key else False}")
