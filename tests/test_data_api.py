import unittest
from unittest.mock import patch
from src.api.data_api import app, fetch_data_from_storage, store_data_in_storage

class TestDataAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @patch('src.api.data_api.fetch_data_from_storage')
    def test_get_data(self, mock_fetch_data):
        mock_fetch_data.return_value = {"data": "Sample data"}
        response = self.app.get('/data')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {"data": "Sample data"})

    @patch('src.api.data_api.store_data_in_storage')
    def test_post_data(self, mock_store_data):
        response = self.app.post('/data', json={"key": "value"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data), {"message": "Data stored successfully"})
        mock_store_data.assert_called_once_with({"key": "value"})

if __name__ == '__main__':
    unittest.main()