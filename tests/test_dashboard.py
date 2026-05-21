import unittest
import pandas as pd
from datetime import datetime, timedelta
from src.cloud_optimize.dashboard import CloudOptimizeDashboard

class TestCloudOptimizeDashboard(unittest.TestCase):
    def setUp(self):
        # Create sample historical data
        self.historical_data = [
            {'date': '2023-01-01', 'cost': 100},
            {'date': '2023-01-02', 'cost': 150},
            {'date': '2023-01-03', 'cost': 200},
            {'date': '2023-01-04', 'cost': 250},
            {'date': '2023-01-05', 'cost': 300},
        ]
        self.dashboard = CloudOptimizeDashboard(self.historical_data)

    def test_display_forecast(self):
        self.dashboard.display_forecast(days=5)

    def test_set_budget(self):
        self.dashboard.set_budget(1000)
        self.assertEqual(self.dashboard.budget, 1000)

    def test_check_budget(self):
        forecast_df = pd.DataFrame({
            'date': [datetime.now() + timedelta(days=i) for i in range(1, 6)],
            'cost': [200, 250, 300, 350, 400]
        })
        self.dashboard.set_budget(1000)
        self.dashboard.check_budget(forecast_df)

if __name__ == '__main__':
    unittest.main()