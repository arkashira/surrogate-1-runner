import unittest
from src.algorithms.build_recommendation import BuildRecommendation

class TestBuildRecommendation(unittest.TestCase):
    def test_get_compatible_components(self):
        budget = 500
        preferences = {"CPU": "Intel", "GPU": "NVIDIA"}
        build_recommendation = BuildRecommendation(budget, preferences)
        compatible_components = build_recommendation.get_compatible_components()

        self.assertEqual(len(compatible_components), 3)

    def test_adjust_recommendations(self):
        budget = 500
        preferences = {"CPU": "Intel", "GPU": "NVIDIA"}
        specific_needs = {"name": "High-performance GPU"}
        build_recommendation = BuildRecommendation(budget, preferences)
        adjusted_components = build_recommendation.adjust_recommendations(specific_needs)

        self.assertEqual(len(adjusted_components), 1)

if __name__ == "__main__":
    unittest.main()