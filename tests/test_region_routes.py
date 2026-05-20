import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestRegionRoutes(unittest.TestCase):
    def test_create_region(self):
        response = client.post('/region/restrictions', json={'region': 'test_region'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Region test_region created')

    def test_get_regions(self):
        response = client.get('/region/restrictions')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['regions'], ['test_region'])

    def test_delete_region(self):
        response = client.delete('/region/restrictions/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Region test_region deleted')

    def test_enable_region(self):
        response = client.post('/region/restrictions/enabled', json={'region': 'test_region'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Region test_region enabled')

    def test_disable_region(self):
        response = client.delete('/region/restrictions/enabled/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Region test_region disabled')

if __name__ == '__main__':
    unittest.main()