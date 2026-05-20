import unittest
from src.analytics.forecast_calculator import ForecastCalculator

class TestForecastCalculator(unittest.TestCase):
    def test_calculate_forecast(self):
        spending_data = [
            {'spend': 100},
            {'spend': 120},
            {'spend': 110},
            {'spend': 130},
            {'spend': 140},
            {'spend': 150},
            {'spend': 160},
            {'spend': 170},
            {'spend': 180},
            {'spend': 190},
            {'spend': 200},
            {'spend': 210},
            {'spend': 220},
            {'spend': 230},
            {'spend': 240},
            {'spend': 250},
        ]
        calculator = ForecastCalculator(spending_data)
        forecast = calculator.calculate_forecast()
        self.assertIsNotNone(forecast)
        self.assertGreaterEqual(forecast['forecast'], 0)
        self.assertGreaterEqual(forecast['ci'], 0)

if __name__ == '__main__':
    unittest.main()