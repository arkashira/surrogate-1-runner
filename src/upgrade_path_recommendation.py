import pandas as pd
from typing import List, Dict

class UpgradePathRecommendation:
    def __init__(self, game_data: pd.DataFrame, budget: float):
        self.game_data = game_data
        self.budget = budget

    def recommend_upgrade_paths(self) -> List[Dict]:
        # Filter games based on budget
        affordable_games = self.game_data[self.game_data['price'] <= self.budget]

        # Sort games by performance impact
        recommended_paths = affordable_games.sort_values(by='performance_impact', ascending=False)

        # Convert to list of dictionaries for easier handling
        recommended_paths_list = recommended_paths.to_dict('records')

        return recommended_paths_list

    def filter_and_sort(self, filters: Dict, sort_by: str) -> List[Dict]:
        # Apply filters
        filtered_paths = self.game_data
        for key, value in filters.items():
            filtered_paths = filtered_paths[filtered_paths[key] == value]

        # Sort by the specified column
        sorted_paths = filtered_paths.sort_values(by=sort_by, ascending=False)

        # Convert to list of dictionaries
        sorted_paths_list = sorted_paths.to_dict('records')

        return sorted_paths_list