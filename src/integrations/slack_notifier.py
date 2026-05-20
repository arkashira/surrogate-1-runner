import requests
import json
from typing import Dict, Any
from config.settings import SLACK_WEBHOOK_URL

class SlackNotifier:
    def __init__(self):
        self.webhook_url = SLACK_WEBHOOK_URL

    def send_alert(self, message: str, rollback_instructions: str) -> bool:
        """
        Sends an alert to Slack with the given message and rollback instructions.

        Args:
            message: The alert message to send.
            rollback_instructions: Instructions on how to rollback the deployment.

        Returns:
            bool: True if the alert was sent successfully, False otherwise.
        """
        payload = {
            "text": message,
            "attachments": [
                {
                    "text": rollback_instructions,
                    "color": "#FF0000"
                }
            ]
        }

        try:
            response = requests.post(
                self.webhook_url,
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Failed to send Slack notification: {e}")
            return False