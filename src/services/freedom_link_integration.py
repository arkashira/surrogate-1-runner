from typing import Dict
import requests

class FreedomLinkIntegration:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.freedomlink.com"

    def link_account(self, team_id: str, user_id: str) -> Dict:
        url = f"{self.base_url}/accounts/link"
        payload = {
            "team_id": team_id,
            "user_id": user_id
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_usage_report(self, team_id: str) -> Dict:
        url = f"{self.base_url}/reports/usage"
        params = {
            "team_id": team_id
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()