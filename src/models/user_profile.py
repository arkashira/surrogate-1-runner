from typing import Dict, List
from datetime import datetime

class UserProfile:
    def __init__(self, user_id: str, usage_data: Dict, preferences: Dict):
        self.user_id = user_id
        self.usage_data = usage_data
        self.preferences = preferences
        self.last_updated = datetime.now()

    def update_usage_data(self, new_usage_data: Dict):
        """Update the usage data for the user."""
        self.usage_data.update(new_usage_data)
        self.last_updated = datetime.now()

    def get_usage_patterns(self) -> Dict:
        """Get the usage patterns for the user."""
        # Implement logic to analyze and return usage patterns
        return {}

    def get_cost_metrics(self) -> Dict:
        """Get the cost metrics for the user."""
        # Implement logic to calculate and return cost metrics
        return {}

    def get_performance_metrics(self) -> Dict:
        """Get the performance metrics for the user."""
        # Implement logic to calculate and return performance metrics
        return {}