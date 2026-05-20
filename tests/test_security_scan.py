import unittest
from unittest.mock import patch, MagicMock
from src.security_scan import SecurityScanner

class TestSecurityScanner(unittest.TestCase):
    @patch('src.security_scan.boto3.client')
    def test_scan_ec2_instances(self, mock_boto_client):
        mock_ec2 = MagicMock()
        mock_boto_client.return_value = mock_ec2

        mock_ec2.describe_instances.return_value = {
            'Reservations': [
                {
                    'Instances': [
                        {
                            'InstanceId': 'i-1234567890abcdef0',
                            'Vulnerabilities': ['Example vulnerability']
                        }
                    ]
                }
            ]
        }

        scanner = SecurityScanner()
        vulnerabilities = scanner.scan_ec2_instances()

        self.assertEqual(len(vulnerabilities), 1)
        self.assertEqual(vulnerabilities[0]['InstanceId'], 'i-1234567890abcdef0')
        self.assertEqual(vulnerabilities[0]['Vulnerabilities'], ['Example vulnerability'])

    @patch('src.security_scan.boto3.client')
    def test_scan_s3_buckets(self, mock_boto_client):
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3

        mock_s3.list_buckets.return_value = {
            'Buckets': [
                {
                    'Name': 'example-bucket',
                    'Vulnerabilities': ['Example vulnerability']
                }
            ]
        }

        scanner = SecurityScanner()
        vulnerabilities = scanner.scan_s3_buckets()

        self.assertEqual(len(vulnerabilities), 1)
        self.assertEqual(vulnerabilities[0]['BucketName'], 'example-bucket')
        self.assertEqual(vulnerabilities[0]['Vulnerabilities'], ['Example vulnerability'])

if __name__ == '__main__':
    unittest.main()