import unittest
from flask import json
from api.terraform_integration import app

class TestTerraformIntegration(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_recommendations(self):
        response = self.app.get('/api/terraform/recommendations')
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertIn('description', data[0])
        self.assertIn('expected_savings_percentage', data[0])
        self.assertIn('implementation_steps', data[0])

    def test_resize_resources(self):
        data = {'terraform_config_path': 'path/to/config'}
        response = self.app.post('/api/terraform/resize', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')

if __name__ == '__main__':
    unittest.main()