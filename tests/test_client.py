import unittest
from unittest.mock import Mock, patch
from sdk.python.client import SurrogateClient, Anomaly

class TestSurrogateClient(unittest.TestCase):
    
    def setUp(self):
        self.client = SurrogateClient("https://api.example.com", "test_api_key")
    
    @patch('sdk.python.client.requests.Session.get')
    def test_get_cost_anomalies(self, mock_get):
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "anomalies": [
                {
                    "id": "anomaly_1",
                    "timestamp": "2023-01-01T00:00:00Z",
                    "amount": 100.0,
                    "threshold": 50.0,
                    "message": "Cost exceeded threshold"
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call method
        result = self.client.get_cost_anomalies()
        
        # Assertions
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Anomaly)
        self.assertEqual(result[0].id, "anomaly_1")
        self.assertEqual(result[0].amount, 100.0)
        self.assertEqual(result[0].threshold, 50.0)
        self.assertEqual(result[0].message, "Cost exceeded threshold")

if __name__ == '__main__':
    unittest.main()