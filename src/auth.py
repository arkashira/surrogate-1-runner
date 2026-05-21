
import hmac
import hashlib
import base64
import secrets
import time

SECRET_KEY = secrets.token_hex(32)

def generate_token(username):
    data = f"{username}.{int(time.time())}".encode("utf-8")
    signature = hmac.new(SECRET_KEY.encode("utf-8"), data, hashlib.sha256).digest()
    token = base64.b64encode(signature).decode("utf-8")
    return token

# /opt/axentx/surrogate-1/src/ai_tools/gpt4.py

import requests
import json

def access_gpt4(token):
    url = "https://api.openai.com/v1/completions"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4",
        "prompt": "You are a helpful assistant.",
        "max_tokens": 100,
        "temperature": 0.9
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        return None