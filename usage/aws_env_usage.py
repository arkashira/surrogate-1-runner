
import boto3
from datetime import datetime, timedelta

class AWSEnvUsage:
    def __init__(self, region_name):
        self.ec2 = boto3.client('ec2', region_name=region_name)
        self.cloudwatch = boto3.client('cloudwatch', region_name=region_name)

    def get_usage(self, instance_id):
        response = self.ec2.describe_instance_status(InstanceIds=[instance_id])
        state = response['InstanceStatuses'][0]['InstanceState']['Name']

        if state != 'running':
            return 0

        now = datetime.utcnow()
        thirty_days_ago = now - timedelta(days=30)

        response = self.cloudwatch.get_metric_statistics(
            Period=86400,
            StartTime=thirty_days_ago,
            EndTime=now,
            MetricName='CPUUtilization',
            Namespace='AWS/EC2',
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}]
        )

        usage = sum([data['Sum'] for data in response['Datapoints']])
        return usage / 30

# /opt/axentx/surrogate-1/usage/test_aws_env_usage.py

import unittest
from usage.aws_env_usage import AWSEnvUsage

class TestAWSEnvUsage(unittest.TestCase):
    def setUp(self):
        self.usage = AWSEnvUsage('us-west-2')

    def test_get_usage(self):
        # Mock test cases here
        pass

## Summary
- Created `AWSEnvUsage` class to track AWS environment usage.
- Added unit test file for `AWSEnvUsage` class.
- Test cases need to be implemented based on the actual AWS environment.