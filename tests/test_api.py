import unittest
from fastapi.testclient import TestClient
from src.api import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_anomalies(self):
        response = self.client.get("/anomalies")
        self.assertEqual(response.status_code, 200)
        self.assertIn("anomalies", response.json())

if __name__ == '__main__':
    unittest.main()