import unittest
from unittest.mock import patch, MagicMock
from src.services.sync_service import SyncService

class TestSyncService(unittest.TestCase):
    def setUp(self):
        self.s3_bucket = 'test-bucket'
        self.s3_key = 'test-key'
        self.encryption_key = Fernet.generate_key()
        self.sync_service = SyncService(self.s3_bucket, self.s3_key, self.encryption_key)
        self.test_data = {'key': 'value'}

    @patch('boto3.client')
    def test_upload_to_s3(self, mock_boto3):
        mock_s3 = MagicMock()
        mock_boto3.return_value = mock_s3
        result = self.sync_service.upload_to_s3(self.test_data)
        self.assertTrue(result)
        mock_s3.put_object.assert_called_once()

    @patch('boto3.client')
    def test_download_from_s3(self, mock_boto3):
        mock_s3 = MagicMock()
        mock_s3.get_object.return_value = {'Body': MagicMock(read=MagicMock(return_value=self.sync_service.encrypt_data(self.test_data)))}
        mock_boto3.return_value = mock_s3
        result = self.sync_service.download_from_s3()
        self.assertEqual(result, self.test_data)

    @patch('boto3.client')
    def test_get_sync_status(self, mock_boto3):
        mock_s3 = MagicMock()
        mock_s3.head_object.return_value = {
            'LastModified': datetime.now(),
            'ContentLength': 1024
        }
        mock_boto3.return_value = mock_s3
        result = self.sync_service.get_sync_status()
        self.assertIn('last_backup', result)
        self.assertIn('size', result)

if __name__ == '__main__':
    unittest.main()