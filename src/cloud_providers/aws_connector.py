import boto3
from datetime import datetime

class AWSConnector:
    def __init__(self, access_key, secret_key, region):
        self.client = boto3.client(
            'ce',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

    def get_costs(self, start_date, end_date, granularity='MONTHLY'):
        response = self.client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity=granularity,
            Metrics=['UnblendedCost']
        )
        return response['ResultsByTime']