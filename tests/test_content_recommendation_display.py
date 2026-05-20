import unittest
from content_recommendation_display import ContentRecommendationDisplay

class TestContentRecommendationDisplay(unittest.TestCase):
    def setUp(self):
        self.user_profile = {'goal': 'increase_brand_awareness'}
        self.display = ContentRecommendationDisplay(self.user_profile)

    def test_load_content_library(self):
        self.display.load_content_library()
        self.assertTrue(len(self.display.content_library) > 0)

    def test_recommend_content(self):
        self.display.load_content_library()
        recommendations = self.display.recommend_content()
        self.assertTrue(len(recommendations) > 0)

    def test_display_recommendations(self):
        self.display.load_content_library()
        recommendations = self.display.recommend_content()
        self.display.display_recommendations()
        # Assuming print statements are captured and checked here

if __name__ == '__main__':
    unittest.main()