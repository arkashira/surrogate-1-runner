import os
import json

class AxentxSDK:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.axentx.com"

    def add_rag(self, rag_data):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(f"{self.base_url}/rag", headers=headers, data=json.dumps(rag_data))
        return response.json()

    def get_rag(self, rag_id):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.get(f"{self.base_url}/rag/{rag_id}", headers=headers)
        return response.json()