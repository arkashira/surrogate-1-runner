import unittest
from src.forecasting.model import train_and_forecast
from src.forecasting.data import get_prepared_data

class TestForecasting(unittest.TestCase):
    def setUp(self):
        self.data_path = 'path/to/historical_cost_data.csv'

    def test_model_training(self):
        model = train_and_forecast(self.data_path)
        self.assertIsNotNone(model)

    def test_data_preparation(self):
        X_train, X_test, y_train, y_test = get_prepared_data(self.data_path)
        self.assertIsNotNone(X_train)
        self.assertIsNotNone(X_test)
        self.assertIsNotNone(y_train)
        self.assertIsNotNone(y_test)


if __name__ == '__main__':
    unittest.main()