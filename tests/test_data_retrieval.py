import unittest
import os
from unittest.mock import patch, MagicMock
from src.data_retrieval import DataRetrieval

class TestDataRetrieval(unittest.TestCase):
    @patch('src.data_retrieval.BlobServiceClient')
    def setUp(self, mock_blob_service_client):
        self.connection_string = "DefaultEndpointsProtocol=https;AccountName=testaccount;AccountKey=testkey;EndpointSuffix=core.windows.net"
        self.container_name = "test-container"
        self.data_retrieval = DataRetrieval(self.connection_string, self.container_name)
        self.mock_blob_service_client = mock_blob_service_client
        self.mock_container_client = MagicMock()
        self.mock_blob_service_client.from_connection_string.return_value = self.mock_blob_service_client
        self.mock_blob_service_client.get_container_client.return_value = self.mock_container_client

    @patch('src.data_retrieval.json')
    def test_retrieve_data(self, mock_json):
        blob_name = "20230505120000_2063c1608d6e0baf80249c42e2be5804.json"
        mock_data = {"key": "value"}
        mock_json.loads.return_value = mock_data
        self.mock_container_client.get_blob_client.return_value.download_blob.return_value.readall.return_value = mock_data
        result = self.data_retrieval.retrieve_data(blob_name)
        self.assertEqual(result, mock_data)

if __name__ == '__main__':
    unittest.main()