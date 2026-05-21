
import requests

class GPT4:
    def __init__(self):
        self.base_url = "https://api.example.com/gpt4"
        self.headers = {"Authorization": "Bearer YOUR_API_KEY"}

    def get_response(self, prompt):
        response = requests.post(f"{self.base_url}", json={"prompt": prompt}, headers=self.headers)
        return response.json()["response"]

# /opt/axentx/surrogate-1/src/ai_tools/__init__.py

from .gpt4 import GPT4

ai_tools = {"gpt4": GPT4}