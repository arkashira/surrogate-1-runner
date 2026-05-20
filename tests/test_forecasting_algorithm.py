import unittest
from src.forecasting_algorithm import load_historical_usage, train_model, generate_forecast

class TestForecastingAlgorithm(unittest.TestCase):
    def test_load_historical_usage(self):
        data = load_historical_usage()
        self.assertIsInstance(data, pd.DataFrame)
    
    def test_train_model(self):
        data = pd.DataFrame({'feature1': [1, 2, 3], 'feature2': [4, 5, 6], 'usage': [7, 8, 9]})
        model, mse = train_model(data)
        self.assertIsInstance(model, LinearRegression)
        self.assertIsInstance(mse, float)
    
    def test_generate_forecast(self):
        data = pd.DataFrame({'feature1': [1, 2, 3], 'feature2': [4, 5, 6]})
        model = LinearRegression()
        model.fit(data.drop('feature2', axis=1), data['feature2'])
        forecast = generate_forecast(model, data)
        self.assertIsInstance(forecast, list)

if __name__ == '__main__':
    unittest.main()