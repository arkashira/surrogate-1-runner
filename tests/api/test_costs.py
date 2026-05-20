import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify
from app import app, db
from models import CostSummary

class TestCostsEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.get_cost_summary')
    def test_get_costs_summary(self, mock_get_cost_summary):
        mock_get_cost_summary.return_value = [
            {'provider': 'AWS', 'service': 'EC2', 'cost': 100},
            {'provider': 'GCP', 'service': 'Compute Engine', 'cost': 150}
        ]
        
        response = self.app.get('/api/v1/costs/summary?hours=24')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['provider'], 'AWS')
        self.assertEqual(data[0]['service'], 'EC2')
        self.assertEqual(data[0]['cost'], 100)
        self.assertEqual(data[1]['provider'], 'GCP')
        self.assertEqual(data[1]['service'], 'Compute Engine')
        self.assertEqual(data[1]['cost'], 150)

    def test_missing_auth(self):
        with patch.object(app, 'auth_required', return_value=False):
            response = self.app.get('/api/v1/costs/summary?hours=24')
            self.assertEqual(response.status_code, 401)

    def test_malformed_query(self):
        response = self.app.get('/api/v1/costs/summary?hours=invalid')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()