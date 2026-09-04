import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print("GEMINI_API_KEY loaded successfully.")
    print("Key starts with:", api_key[:8])
else:
    print("GEMINI_API_KEY was not found.")