import unittest
from unittest.mock import Mock
from src.services.dashboard import Dashboard

class TestDashboard(unittest.TestCase):
    def setUp(self):
        self.dashboard = Dashboard()

    def test_fetch_data(self):
        costinel_response = Mock()
        costinel_response.text = '{"accounts": [{"spend": 100, "budget": 1000}, {"spend": 200, "budget": 2000}]}'
        surrogate_1_response = Mock()
        surrogate_1_response.text = '{"accounts": [{"spend": 300, "budget": 3000}, {"spend": 400, "budget": 4000}]}'

        self.dashboard.costinel_api_url = "https://api.costinel.com/v1"
        self.dashboard.surrogate_1_api_url = "https://api.surrogate-1.com/v1"

        self.dashboard.costinel_response = costinel_response
        self.dashboard.surrogate_1_response = surrogate_1_response

        costinel_data, surrogate_1_data = self.dashboard.fetch_data()

        self.assertEqual(len(costinel_data), 2)
        self.assertEqual(len(surrogate_1_data), 2)

    def test_calculate_health_score(self):
        account_data = [{"spend": 100, "budget": 1000}, {"spend": 200, "budget": 2000}]
        health_score = self.dashboard.calculate_health_score(account_data)
        self.assertGreater(health_score, 0.8)

if __name__ == "__main__":
    unittest.main()