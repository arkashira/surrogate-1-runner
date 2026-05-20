import unittest
from flask import Flask
from api.routes.consolidated import consolidated_bp

class TestConsolidatedAlerts(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(consolidated_bp)
        self.client = self.app.test_client()

    def test_get_consolidated_alerts(self):
        response = self.client.get('/api/consolidated_alerts')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertLessEqual(len(response.json), 1000)

if __name__ == '__main__':
    unittest.main()