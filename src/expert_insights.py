import requests
from datetime import datetime

class ExpertInsights:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.expertinsights.com/v1"

    def get_insights(self, component_id):
        url = f"{self.base_url}/insights/{component_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch insights: {response.status_code}")

    def validate_insights(self, insights):
        if not insights.get("validated"):
            raise Exception("Insights not validated by expert")
        if insights.get("expiry_date") < datetime.now().isoformat():
            raise Exception("Insights are outdated")

    def moderate_insights(self, insights):
        if insights.get("moderation_status") != "approved":
            raise Exception("Insights not approved by moderator")

    def get_validated_insights(self, component_id):
        insights = self.get_insights(component_id)
        self.validate_insights(insights)
        self.moderate_insights(insights)
        return insights