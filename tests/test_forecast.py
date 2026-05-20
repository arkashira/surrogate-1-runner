import unittest
import pandas as pd
from datetime import datetime, timedelta
from services.forecast import CloudSpendingForecaster

class TestCloudSpendingForecaster(unittest.TestCase):
    def setUp(self):
        # Create sample historical data
        dates = [datetime(2023, 1, 1) + timedelta(days=x) for x in range(30)]
        spending = [100 + x * 2 for x in range(30)]
        self.historical_data = pd.DataFrame({'date': dates, 'spending': spending})

    def test_preprocess_data(self):
        forecaster = CloudSpendingForecaster(self.historical_data)
        forecaster.preprocess_data()
        self.assertEqual(len(forecaster.historical_data), 29)  # Check for differencing

    def test_train_model(self):
        forecaster = CloudSpendingForecaster(self.historical_data)
        forecaster.train_model()
        self.assertIsNotNone(forecaster.model)
        self.assertIsNotNone(forecaster.forecast)

    def test_generate_forecast(self):
        forecaster = CloudSpendingForecaster(self.historical_data)
        forecast_data = forecaster.generate_forecast()
        self.assertEqual(len(forecast_data), 90)  # Check for 90-day forecast
        self.assertIn('forecast', forecast_data.columns)
        self.assertIn('lower_ci', forecast_data.columns)
        self.assertIn('upper_ci', forecast_data.columns)

    def test_export_to_csv(self):
        forecaster = CloudSpendingForecaster(self.historical_data)
        forecast_data = forecaster.generate_forecast()
        forecaster.export_to_csv(forecast_data)
        self.assertTrue(os.path.exists('cloud_spending_forecast.csv'))

if __name__ == '__main__':
    unittest.main()