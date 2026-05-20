import unittest
import json
from src.api.forecast import forecast_blueprint
from app import create_app

class TestForecast(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_get_forecast(self):
        response = self.client.get('/forecast')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 30)
        self.assertIn('date', data[0])
        self.assertIn('predicted_cost', data[0])
        self.assertIn('confidence_interval', data[0])

    def test_get_forecast_with_custom_data_path(self):
        response = self.client.get('/forecast?data_path=custom_data.csv')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 30)
        self.assertIn('date', data[0])
        self.assertIn('predicted_cost', data[0])
        self.assertIn('confidence_interval', data[0])

if __name__ == '__main__':
    unittest.main()