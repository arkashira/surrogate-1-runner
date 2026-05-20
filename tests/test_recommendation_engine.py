import unittest
import json
import os
from recommendation_engine import RecommendationEngine

class TestRecommendationEngine(unittest.TestCase):
    def setUp(self):
        self.test_content_library = {
            "marketing": [
                {"id": 1, "title": "Social Media Guide", "tags": ["social_media"]},
                {"id": 2, "title": "Email Marketing Tips", "tags": ["email_marketing"]}
            ],
            "sales": [
                {"id": 3, "title": "Lead Generation Strategies", "tags": ["lead_generation"]}
            ]
        }
        self.test_library_path = "test_content_library.json"
        with open(self.test_library_path, 'w') as f:
            json.dump(self.test_content_library, f)

        self.engine = RecommendationEngine(self.test_library_path)

    def tearDown(self):
        if os.path.exists(self.test_library_path):
            os.remove(self.test_library_path)
        if os.path.exists("test_recommendations.json"):
            os.remove("test_recommendations.json")

    def test_generate_recommendations(self):
        self.engine.set_business_needs({
            "marketing": "social_media,email_marketing",
            "sales": "lead_generation"
        })
        self.engine.set_goals({
            "short_term": "increase_website_traffic",
            "long_term": "build_brand_awareness"
        })
        recommendations = self.engine.generate_recommendations()
        self.assertEqual(len(recommendations), 3)

    def test_save_recommendations(self):
        self.engine.set_business_needs({
            "marketing": "social_media",
            "sales": ""
        })
        recommendations = self.engine.generate_recommendations()
        self.engine.save_recommendations(recommendations, "test_recommendations.json")
        self.assertTrue(os.path.exists("test_recommendations.json"))

    def test_matches_needs(self):
        item = {"id": 1, "title": "Social Media Guide", "tags": ["social_media"]}
        self.assertTrue(self.engine._matches_needs(item, "marketing"))

    def test_rank_recommendations(self):
        recommendations = [
            {"id": 1, "title": "Social Media Guide", "tags": ["social_media"]},
            {"id": 2, "title": "Email Marketing Tips", "tags": ["email_marketing"]},
            {"id": 3, "title": "Lead Generation Strategies", "tags": ["lead_generation"]}
        ]
        ranked = self.engine._rank_recommendations(recommendations)
        self.assertEqual(len(ranked), 3)

if __name__ == "__main__":
    unittest.main()