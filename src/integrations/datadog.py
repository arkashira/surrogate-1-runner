import requests
from typing import Dict, Any

class DatadogIntegration:
    def __init__(self, api_key: str, app_key: str):
        self.api_key = api_key
        self.app_key = app_key
        self.base_url = "https://api.datadoghq.com/api/v1"

    def create_event(self, title: str, text: str, tags: Dict[str, str] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/events"
        headers = {
            "Content-Type": "application/json",
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key
        }
        payload = {
            "title": title,
            "text": text,
            "tags": tags if tags else {}
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def get_event(self, event_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/events/{event_id}"
        headers = {
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()