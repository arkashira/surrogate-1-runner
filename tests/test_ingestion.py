import unittest
from unittest.mock import patch, MagicMock
import time
from datetime import datetime

# Mock the external dependencies
with patch('boto3.client'):
    from src.ingestion_worker import start_ingestion_job

class TestIngestionStart(unittest.TestCase):

    @patch('src.ingestion_worker.s3_client')
    @patch('src.ingestion_worker.logging')
    def test_start_ingestion_job_success(self, mock_logging, mock_s3_client):
        """Test that ingestion job starts successfully within 5 seconds"""
        # Setup mocks
        mock_s3_client.put_object.return_value = {'ETag': 'test-etag'}
        mock_logging.info = MagicMock()

        # Capture start time
        start_time = time.time()

        # Call the function
        result = start_ingestion_job("test_dataset", "test_bucket")

        # Check timing constraint
        end_time = time.time()
        execution_time = end_time - start_time

        # Verify it completed within 5 seconds
        self.assertLessEqual(execution_time, 5.0)

        # Verify S3 upload was called
        mock_s3_client.put_object.assert_called_once()

        # Verify logging was called
        mock_logging.info.assert_called()

        # Verify return value
        self.assertTrue(result)

    @patch('src.ingestion_worker.s3_client')
    @patch('src.ingestion_worker.logging')
    def test_start_ingestion_job_with_correct_key(self, mock_logging, mock_s3_client):
        """Test that dataset is stored with correct S3 key"""
        mock_s3_client.put_object.return_value = {'ETag': 'test-etag'}
        mock_logging.info = MagicMock()

        dataset_name = "sample_dataset"
        bucket_name = "test-bucket"

        start_ingestion_job(dataset_name, bucket_name)

        # Verify the S3 key format
        call_args = mock_s3_client.put_object.call_args
        s3_key = call_args[1]['Key']

        # Should contain dataset name and timestamp
        self.assertIn(dataset_name, s3_key)
        self.assertIn(str(datetime.now().year), s3_key)

        # Verify bucket name
        self.assertEqual(call_args[1]['Bucket'], bucket_name)

if __name__ == '__main__':
    unittest.main()