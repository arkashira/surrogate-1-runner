import unittest
from flask import Flask
from api.routes.cost_forecast import register_routes

class TestCostForecast(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        register_routes(self.app)
        self.client = self.app.test_client()

    def test_get_cost_forecast_valid_provider(self):
        response = self.client.get('/v1/costs/forecast?provider=aws')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(isinstance(data, list))
        self.assertTrue(all('date' in item and 'amount_usd' in item for item in data))

    def test_get_cost_forecast_invalid_provider(self):
        response = self.client.get('/v1/costs/forecast?provider=invalid')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

if __name__ == '__main__':
    unittest.main()