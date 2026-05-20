import unittest
import os
from unittest.mock import patch, MagicMock
from src.data_ingestion import DataIngestion

class TestDataIngestion(unittest.TestCase):
    @patch('src.data_ingestion.BlobServiceClient')
    def setUp(self, mock_blob_service_client):
        self.connection_string = "DefaultEndpointsProtocol=https;AccountName=testaccount;AccountKey=testkey;EndpointSuffix=core.windows.net"
        self.container_name = "test-container"
        self.data_ingestion = DataIngestion(self.connection_string, self.container_name)
        self.mock_blob_service_client = mock_blob_service_client
        self.mock_container_client = MagicMock()
        self.mock_blob_service_client.from_connection_string.return_value = self.mock_blob_service_client
        self.mock_blob_service_client.get_container_client.return_value = self.mock_container_client

    def test_generate_md5_hash(self):
        data = {"key": "value"}
        expected_hash = "2063c1608d6e0baf80249c42e2be5804"
        self.assertEqual(self.data_ingestion.generate_md5_hash(data), expected_hash)

    @patch('src.data_ingestion.datetime')
    def test_ingest_data(self, mock_datetime):
        mock_datetime.now.return_value.strftime.return_value = "20230505120000"
        data = {"key": "value"}
        expected_blob_name = "20230505120000_2063c1608d6e0baf80249c42e2be5804.json"
        self.data_ingestion.ingest_data(data)
        self.mock_container_client.get_blob_client.assert_called_once_with(expected_blob_name)

if __name__ == '__main__':
    unittest.main()