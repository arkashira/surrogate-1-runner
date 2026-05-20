import unittest
from unittest.mock import patch
from src.api.validate import validate_s3_connection, app

class TestValidateConnection(unittest.TestCase):

    @patch('src.api.validate.boto3.client')
    def test_valid_s3_connection(self, mock_boto3_client):
        mock_head_bucket = mock_boto3_client.return_value.head_bucket
        mock_head_bucket.return_value = {}
        result, _ = validate_s3_connection("test-bucket", "test-key", "test-secret")
        self.assertTrue(result)

    @patch('src.api.validate.boto3.client')
    def test_invalid_s3_connection(self, mock_boto3_client):
        mock_head_bucket = mock_boto3_client.return_value.head_bucket
        mock_head_bucket.side_effect = Exception("Invalid credentials")
        result, error_message = validate_s3_connection("test-bucket", "test-key", "test-secret")
        self.assertFalse(result)
        self.assertEqual(error_message, "Invalid credentials")

    def test_missing_parameters(self):
        with app.test_client() as client:
            response = client.post('/api/validate-connection', json={})
            self.assertEqual(response.status_code, 400)
            self.assertIn("Missing required parameters", response.json['error'])

if __name__ == '__main__':
    unittest.main()