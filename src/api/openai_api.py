import requests
from typing import List, Dict, Optional

class OpenAIApi:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def get_models(self) -> List[Dict]:
        """Fetch all available OpenAI models."""
        response = requests.get("https://api.openai.com/v1/models", headers=self.headers)
        response.raise_for_status()
        return response.json()["data"]

    def get_model_info(self, model_id: str) -> "OpenAIModelInfo":
        """Retrieve detailed information for a specific model."""
        response = requests.get(f"https://api.openai.com/v1/models/{model_id}", headers=self.headers)
        response.raise_for_status()
        model_data = response.json()["data"]
        return OpenAIModelInfo(
            id=model_data["id"],
            name=model_data["name"],
            owned_by=model_data["owned_by"],
            permission=model_data.get("permission", []),
            root=model_data.get("root", ""),
            parent=model_data.get("parent", None),
            created=model_data.get("created", 0)
        )