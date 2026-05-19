import unittest
import pandas as pd
from src.upgrade_path_recommendation import UpgradePathRecommendation

class TestUpgradePathRecommendation(unittest.TestCase):
    def setUp(self):
        data = {
            'game': ['Game A', 'Game B', 'Game C', 'Game D'],
            'price': [100, 200, 150, 50],
            'performance_impact': [0.8, 0.7, 0.9, 0.6],
            'genre': ['Action', 'RPG', 'Action', 'Adventure']
        }
        self.game_data = pd.DataFrame(data)
        self.recommender = UpgradePathRecommendation(self.game_data, 150)

    def test_recommend_upgrade_paths(self):
        recommended_paths = self.recommender.recommend_upgrade_paths()
        self.assertEqual(len(recommended_paths), 3)
        self.assertEqual(recommended_paths[0]['game'], 'Game C')

    def test_filter_and_sort(self):
        filters = {'genre': 'Action'}
        sorted_paths = self.recommender.filter_and_sort(filters, 'performance_impact')
        self.assertEqual(len(sorted_paths), 2)
        self.assertEqual(sorted_paths[0]['game'], 'Game C')

if __name__ == '__main__':
    unittest.main()