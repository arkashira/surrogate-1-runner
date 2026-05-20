import requests
from typing import Dict, Any

class PagerDutyIntegration:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.pagerduty.com"

    def create_incident(self, service_id: str, title: str, description: str) -> Dict[str, Any]:
        url = f"{self.base_url}/incidents"
        headers = {
            "Authorization": f"Token token={self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.pagerduty+json;version=2"
        }
        payload = {
            "incident": {
                "type": "incident",
                "title": title,
                "service": {
                    "id": service_id,
                    "type": "service_reference"
                },
                "body": {
                    "type": "incident_body",
                    "details": description
                }
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def get_incident(self, incident_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/incidents/{incident_id}"
        headers = {
            "Authorization": f"Token token={self.api_key}",
            "Accept": "application/vnd.pagerduty+json;version=2"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()