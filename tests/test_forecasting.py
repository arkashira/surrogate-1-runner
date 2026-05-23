import unittest
import numpy as np
from src.forecasting import ForecastModel

class TestForecastModel(unittest.TestCase):
    def setUp(self):
        self.historical_data = [100, 105, 110, 115, 120, 125, 130, 135, 140, 145]
        self.model = ForecastModel(self.historical_data)
        self.model.train()

    def test_train(self):
        self.assertIsNotNone(self.model.model.coef_)
        self.assertIsNotNone(self.model.model.intercept_)

    def test_predict(self):
        forecast = self.model.predict(5)
        self.assertEqual(len(forecast), 5)
        self.assertTrue(all(isinstance(x, np.float64) for x in forecast))

    def test_plot_forecast(self):
        forecast = self.model.predict(5)
        try:
            self.model.plot_forecast(forecast)
        except Exception as e:
            self.fail(f"plot_forecast raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()