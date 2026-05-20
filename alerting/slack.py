import os
import yaml
import requests
from typing import Dict, Any

class SlackAlert:
    def __init__(self):
        self.secrets = self._load_secrets()
        self.webhook_url = self.secrets.get('slack_webhook_url')

    def _load_secrets(self) -> Dict[str, Any]:
        with open('/opt/axentx/surrogate-1/config/secrets.yaml', 'r') as file:
            return yaml.safe_load(file)

    def send_alert(self, message: str, status: str) -> bool:
        if not self.webhook_url:
            return False

        payload = {
            "text": f"Incident Alert: {message}",
            "attachments": [
                {
                    "color": "danger" if status == "failed" else "good",
                    "fields": [
                        {
                            "title": "Remediation Status",
                            "value": status,
                            "short": True
                        }
                    ]
                }
            ]
        }

        response = requests.post(self.webhook_url, json=payload)
        return response.status_code == 200

    def generate_root_cause_summary(self, incident_data: Dict[str, Any]) -> str:
        summary = (
            f"Incident ID: {incident_data.get('id', 'N/A')}\n"
            f"Root Cause: {incident_data.get('root_cause', 'Unknown')}\n"
            f"Severity: {incident_data.get('severity', 'Medium')}"
        )
        return summary