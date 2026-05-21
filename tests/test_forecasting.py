import unittest
import pandas as pd
from datetime import datetime, timedelta
from src.cloud_optimize.forecasting import Forecasting

class TestForecasting(unittest.TestCase):
    def setUp(self):
        # Create sample historical data
        self.historical_data = [
            {'date': '2023-01-01', 'cost': 100},
            {'date': '2023-01-02', 'cost': 150},
            {'date': '2023-01-03', 'cost': 200},
            {'date': '2023-01-04', 'cost': 250},
            {'date': '2023-01-05', 'cost': 300},
        ]
        self.forecasting = Forecasting(self.historical_data)

    def test_forecast_costs(self):
        forecast_df = self.forecasting.forecast_costs(days=5)
        self.assertEqual(len(forecast_df), 5)
        self.assertTrue(all(forecast_df['cost'] > 0))

if __name__ == '__main__':
    unittest.main()