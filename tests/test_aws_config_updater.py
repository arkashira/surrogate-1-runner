import unittest
from unittest.mock import patch, MagicMock
from src.aws_config_updater import AWSConfigUpdater

class TestAWSConfigUpdater(unittest.TestCase):
    @patch('boto3.client')
    def setUp(self, mock_boto3):
        self.mock_ec2 = MagicMock()
        self.mock_elbv2 = MagicMock()
        self.mock_rds = MagicMock()
        mock_boto3.side_effect = [self.mock_ec2, self.mock_elbv2, self.mock_rds]
        self.updater = AWSConfigUpdater()

    def test_update_ec2_instance(self):
        self.mock_ec2.modify_instance_attribute.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}
        response = self.updater.update_ec2_instance('i-1234567890', 't2.micro')
        self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)

    def test_update_load_balancer(self):
        self.mock_elbv2.modify_load_balancer_attributes.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}
        response = self.updater.update_load_balancer('arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/my-load-balancer/50dc6c495c0c9188', [{'Key': 'access_logs.s3.enabled', 'Value': 'true'}])
        self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)

    def test_update_rds_instance(self):
        self.mock_rds.modify_db_instance.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}
        response = self.updater.update_rds_instance('my-db-instance', 'db.t2.micro')
        self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='{"ec2_instances": [{"instance_id": "i-1234567890", "instance_type": "t2.micro"}], "load_balancers": [{"load_balancer_arn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/my-load-balancer/50dc6c495c0c9188", "attributes": [{"Key": "access_logs.s3.enabled", "Value": "true"}]}], "rds_instances": [{"db_instance_identifier": "my-db-instance", "db_instance_class": "db.t2.micro"}]}')
    def test_update_configurations(self, mock_open):
        self.mock_ec2.modify_instance_attribute.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}
        self.mock_elbv2.modify_load_balancer_attributes.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}
        self.mock_rds.modify_db_instance.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}
        self.updater.update_configurations('config.json')
        self.mock_ec2.modify_instance_attribute.assert_called_once_with(InstanceId='i-1234567890', InstanceType={'Value': 't2.micro'})
        self.mock_elbv2.modify_load_balancer_attributes.assert_called_once_with(LoadBalancerArn='arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/my-load-balancer/50dc6c495c0c9188', Attributes=[{'Key': 'access_logs.s3.enabled', 'Value': 'true'}])
        self.mock_rds.modify_db_instance.assert_called_once_with(DBInstanceIdentifier='my-db-instance', DBInstanceClass='db.t2.micro', ApplyImmediately=True)

if __name__ == '__main__':
    unittest.main()