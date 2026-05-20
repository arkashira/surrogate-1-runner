import requests
import time
from typing import Optional

class SlackNotifier:
    def __init__(self, webhook_url: str, max_retries: int = 3, initial_delay: float = 1.0):
        self.webhook_url = webhook_url
        self.max_retries = max_retries
        self.initial_delay = initial_delay

    def send_notification(self, message: str) -> bool:
        """Send notification to Slack with retry logic and exponential backoff"""
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.webhook_url,
                    json={"text": message},
                    headers={"Content-Type": "application/json"},
                    timeout=10  # Added timeout for better reliability
                )
                response.raise_for_status()
                return True
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    print(f"Failed to send Slack notification after {self.max_retries} attempts: {e}")
                    return False
                delay = self.initial_delay * (2 ** attempt)
                time.sleep(delay)
        return False

    def send_test_notification(self) -> bool:
        """Send a test notification with standard test message"""
        return self.send_notification("Test notification from Slack Notifier")