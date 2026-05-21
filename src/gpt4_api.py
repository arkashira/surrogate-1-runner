import re
import os

def validate_gpt4_api_key(api_key):
    pattern = r"^[a-zA-Z0-9_-]{32}$"
    if not re.match(pattern, api_key):
        raise ValueError("Invalid GPT-4 API key")
    return api_key

def get_gpt4_api_key():
    api_key = os.environ.get("GPT4_API_KEY")
    if not api_key:
        raise ValueError("GPT-4 API key is not set")
    return validate_gpt4_api_key(api_key)