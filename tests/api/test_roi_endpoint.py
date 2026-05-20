import unittest
from fastapi.testclient import TestClient
from src.api.roi_endpoint import router

class TestROIEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(router)

    def test_get_roi(self):
        response = self.client.get("/roi")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 6)
        self.assertEqual(response.json()[0]['name'], 'GPU A')

    def test_get_roi_filtered(self):
        response = self.client.get("/roi?component_type=GPU")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]['name'], 'GPU A')

if __name__ == '__main__':
    unittest.main()