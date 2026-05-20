import unittest
from unittest.mock import patch
from src.aws_collector import AWSInventoryCollector

class TestAWSInventoryCollector(unittest.TestCase):
    @patch('src.aws_collector.boto3.client')
    def test_collect_ec2_inventory(self, mock_client):
        mock_client.return_value.describe_instances.return_value = {
            'Reservations': [
                {
                    'Instances': [
                        {'InstanceId': 'i-12345678', 'InstanceType': 't2.micro'}
                    ]
                }
            ]
        }
        collector = AWSInventoryCollector('account-id')
        collector.collect_ec2_inventory()
        self.assertEqual(collector.inventory['ec2'], [{'id': 'i-12345678', 'type': 't2.micro'}])

    @patch('src.aws_collector.boto3.client')
    def test_collect_s3_inventory(self, mock_client):
        mock_client.return_value.list_buckets.return_value = {
            'Buckets': [
                {'Name': 'bucket-name'}
            ]
        }
        collector = AWSInventoryCollector('account-id')
        collector.collect_s3_inventory()
        self.assertEqual(collector.inventory['s3'], [{'name': 'bucket-name'}])

if __name__ == '__main__':
    unittest.main()