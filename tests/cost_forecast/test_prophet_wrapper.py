import unittest
import pandas as pd
from datetime import datetime, timedelta
from src.cost_forecast.prophet_wrapper import ProphetWrapper, normalize_data

class TestProphetWrapper(unittest.TestCase):
    def setUp(self):
        self.end_date = datetime.now().date()
        self.start_date = self.end_date - timedelta(days=180)
        self.dates = pd.date_range(start=self.start_date, end=self.end_date)
        self.data = pd.DataFrame({'ds': self.dates, 'amount_usd': [i * 100 for i in range(len(self.dates))]})
        self.normalized_data = normalize_data(self.data)

    def test_normalize_data(self):
        normalized_data = normalize_data(self.data)
        self.assertEqual(len(normalized_data), len(self.data))
        self.assertTrue(all(normalized_data['ds'] == self.data['ds']))
        self.assertTrue(all(normalized_data['y'] == self.data['amount_usd']))

    def test_train_and_forecast(self):
        prophet_wrapper = ProphetWrapper(self.normalized_data)
        prophet_wrapper.train()
        forecast = prophet_wrapper.forecast(periods=30)
        self.assertEqual(len(forecast), 30)
        self.assertTrue(all(forecast['ds'] >= self.end_date))

    def test_backtest(self):
        prophet_wrapper = ProphetWrapper(self.normalized_data)
        prophet_wrapper.train()
        mae = prophet_wrapper.backtest()
        self.assertLess(mae, 0.1 * self.normalized_data['y'].mean())

if __name__ == '__main__':
    unittest.main()