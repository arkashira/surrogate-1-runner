import unittest
import os
import json
from datetime import datetime, timedelta
from cost_forecasting import CostForecaster

class TestCostForecaster(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = 'test_data'
        os.makedirs(self.test_data_dir, exist_ok=True)

        # Create test data files
        for i in range(30):
            date = datetime.now() - timedelta(days=30-i)
            data = {
                'date': date.strftime('%Y-%m-%d'),
                'total_cost': 100 + i * 5,
                'service1': 50 + i * 2,
                'service2': 50 + i * 3
            }
            with open(os.path.join(self.test_data_dir, f'data_{i}.json'), 'w') as f:
                json.dump(data, f)

        self.forecaster = CostForecaster(self.test_data_dir)

    def tearDown(self):
        # Clean up test data files
        for f in os.listdir(self.test_data_dir):
            os.remove(os.path.join(self.test_data_dir, f))
        os.rmdir(self.test_data_dir)

    def test_load_historical_data(self):
        self.forecaster.load_historical_data()
        self.assertIsNotNone(self.forecaster.historical_data)
        self.assertEqual(len(self.forecaster.historical_data), 30)

    def test_preprocess_data(self):
        self.forecaster.preprocess_data()
        self.assertIsNotNone(self.forecaster.historical_data)
        self.assertEqual(self.forecaster.historical_data.index[0].date(), datetime.now().date() - timedelta(days=30))
        self.assertEqual(self.forecaster.historical_data.index[-1].date(), datetime.now().date() - timedelta(days=1))

    def test_generate_forecast(self):
        self.forecaster.generate_forecast(days=7)
        self.assertIsNotNone(self.forecaster.forecast_data)
        self.assertEqual(len(self.forecaster.forecast_data), 7)
        self.assertEqual(self.forecaster.forecast_data['date'].iloc[0].date(), datetime.now().date())

    def test_save_forecast(self):
        self.forecaster.generate_forecast(days=7)
        self.forecaster.save_forecast('test_forecast.json')
        self.assertTrue(os.path.exists('test_forecast.json'))
        os.remove('test_forecast.json')

    def test_update_forecast_daily(self):
        self.forecaster.update_forecast_daily()
        self.assertTrue(os.path.exists('forecast.json'))
        os.remove('forecast.json')

if __name__ == '__main__':
    unittest.main()