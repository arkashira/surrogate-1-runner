import os
import requests
from typing import List, Dict
from repository_selector_config import GITHUB_API_URL, GITHUB_TOKEN

class RepositorySelector:
    def __init__(self):
        self.github_token = GITHUB_TOKEN
        self.headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def get_user_repositories(self) -> List[Dict]:
        """Fetch all repositories for the authenticated user."""
        url = f"{GITHUB_API_URL}/user/repos"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def connect_repository(self, repo_name: str) -> bool:
        """Connect a specific repository to the Workflow Automation Accelerator."""
        # Here you would implement the logic to connect the repository
        # For now, we'll just return True to simulate success
        return True

    def get_connected_repositories(self) -> List[Dict]:
        """Retrieve the list of connected repositories from the dashboard."""
        # Here you would implement the logic to fetch connected repositories
        # For now, we'll return an empty list
        return []