import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from bin.gcp_cost_ingestion import fetch_cost_data, upload_to_gcs

class TestGCPCostIngestion(unittest.TestCase):

    @patch('bin.gcp_cost_ingestion.bigquery.Client')
    def test_fetch_cost_data(self, mock_client):
        mock_query_job = MagicMock()
        mock_query_job.result.return_value = [MagicMock()]
        mock_client.return_value.query.return_value = mock_query_job

        start_time = datetime.utcnow() - timedelta(minutes=15)
        end_time = datetime.utcnow()
        result = fetch_cost_data(start_time, end_time)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    @patch('bin.gcp_cost_ingestion.storage.Client')
    def test_upload_to_gcs(self, mock_client):
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_client.return_value.bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob

        data = [{"cost": 100}]
        upload_to_gcs(data, "test-bucket", "test-blob")

        mock_blob.upload_from_string.assert_called_once()

if __name__ == '__main__':
    unittest.main()