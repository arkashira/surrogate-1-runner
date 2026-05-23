import unittest
from datetime import datetime, timedelta
from src.cost_forecast.cost_forecast import generate_cost_forecast

class TestCostForecast(unittest.TestCase):
    def test_generate_cost_forecast(self):
        forecast = generate_cost_forecast()
        self.assertEqual(len(forecast), 30)
        end_date = datetime.now().date()
        expected_dates = [end_date + timedelta(days=i) for i in range(1, 31)]
        forecast_dates = [item['ds'].date() for item in forecast]
        self.assertEqual(forecast_dates, expected_dates)

if __name__ == '__main__':
    unittest.main()