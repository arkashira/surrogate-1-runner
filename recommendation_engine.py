import json
import random
from typing import Dict, List, Optional

class RecommendationEngine:
    def __init__(self, content_library_path: str):
        self.content_library = self._load_content_library(content_library_path)
        self.business_needs = {}
        self.goals = {}

    def _load_content_library(self, path: str) -> Dict[str, List[Dict]]:
        with open(path, 'r') as f:
            return json.load(f)

    def set_business_needs(self, needs: Dict[str, str]):
        self.business_needs = needs

    def set_goals(self, goals: Dict[str, str]):
        self.goals = goals

    def generate_recommendations(self) -> List[Dict]:
        if not self.business_needs or not self.goals:
            raise ValueError("Business needs and goals must be set before generating recommendations")

        recommendations = []
        for category, content in self.content_library.items():
            for item in content:
                if self._matches_needs(item, category):
                    recommendations.append(item)

        return self._rank_recommendations(recommendations)

    def _matches_needs(self, item: Dict, category: str) -> bool:
        item_tags = set(item.get('tags', []))
        needs_tags = set(self.business_needs.get(category, '').split(','))

        if not needs_tags:
            return True

        return bool(item_tags & needs_tags)

    def _rank_recommendations(self, recommendations: List[Dict]) -> List[Dict]:
        ranked = sorted(recommendations, key=lambda x: random.random())
        return ranked[:5]  # Return top 5 recommendations

    def save_recommendations(self, recommendations: List[Dict], output_path: str):
        with open(output_path, 'w') as f:
            json.dump(recommendations, f, indent=2)

# Example usage
if __name__ == "__main__":
    engine = RecommendationEngine("content_library.json")
    engine.set_business_needs({
        "marketing": "social_media,email_marketing",
        "sales": "lead_generation"
    })
    engine.set_goals({
        "short_term": "increase_website_traffic",
        "long_term": "build_brand_awareness"
    })
    recommendations = engine.generate_recommendations()
    engine.save_recommendations(recommendations, "recommendations.json")