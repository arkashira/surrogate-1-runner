import requests
from typing import Dict, Any

class SlackIntegration:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_message(self, text: str, channel: str = None, username: str = None) -> Dict[str, Any]:
        payload = {
            "text": text,
            "channel": channel if channel else "#general",
            "username": username if username else "surrogate-1"
        }
        response = requests.post(self.webhook_url, json=payload)
        response.raise_for_status()
        return response.json()