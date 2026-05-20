from typing import Dict
from .services.freedom_link_integration import FreedomLinkIntegration

class TeamManagement:
    def __init__(self, freedom_link_api_key: str):
        self.freedom_link_integration = FreedomLinkIntegration(freedom_link_api_key)

    def create_team_account(self, team_id: str, user_id: str) -> Dict:
        return self.freedom_link_integration.link_account(team_id, user_id)

    def get_team_usage_report(self, team_id: str) -> Dict:
        return self.freedom_link_integration.get_usage_report(team_id)