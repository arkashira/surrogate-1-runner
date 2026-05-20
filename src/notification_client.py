from typing import Dict, Any
import requests

class NotificationClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def send_notification(self, notification: Dict[str, Any]) -> bool:
        try:
            response = requests.post(self.api_url, json=notification, timeout=10)
            if response.status_code == 200:
                return True
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Connection Error: {e}")
            return False