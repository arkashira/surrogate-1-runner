import requests
from typing import Dict, Any

class ExpertInsights:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.expertinsights.com/v1"

    def get_insights(self, component_id: str) -> Dict[str, Any]:
        """
        Fetch expert insights for a given component.

        Args:
            component_id (str): The ID of the component to fetch insights for.

        Returns:
            Dict[str, Any]: A dictionary containing the expert insights.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.get(f"{self.base_url}/insights/{component_id}", headers=headers)
        response.raise_for_status()
        return response.json()

    def get_recommendations(self, component_id: str) -> Dict[str, Any]:
        """
        Fetch expert recommendations for a given component.

        Args:
            component_id (str): The ID of the component to fetch recommendations for.

        Returns:
            Dict[str, Any]: A dictionary containing the expert recommendations.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.get(f"{self.base_url}/recommendations/{component_id}", headers=headers)
        response.raise_for_status()
        return response.json()