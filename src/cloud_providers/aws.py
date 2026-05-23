import boto3
from datetime import datetime, timedelta

class AWSCostExplorer:
    def __init__(self):
        self.client = boto3.client('ce')

    def get_real_time_cost(self, start_date=None, end_date=None):
        if not start_date:
            start_date = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.utcnow().strftime('%Y-%m-%d')

        response = self.client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='HOURLY',
            Metrics=['UnblendedCost'],
            Filter={
                'Dimensions': {
                    'Key': 'SERVICE',
                    'Values': ['Amazon Elastic Compute Cloud - Compute']
                }
            }
        )
        return response['ResultsByTime']

    def filter_cost_by_resource_type(self, resource_type, start_date=None, end_date=None):
        response = self.client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='HOURLY',
            Metrics=['UnblendedCost'],
            Filter={
                'Dimensions': {
                    'Key': 'SERVICE',
                    'Values': [resource_type]
                }
            }
        )
        return response['ResultsByTime']

    def filter_cost_by_location(self, location, start_date=None, end_date=None):
        response = self.client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='HOURLY',
            Metrics=['UnblendedCost'],
            Filter={
                'Dimensions': {
                    'Key': 'REGION',
                    'Values': [location]
                }
            }
        )
        return response['ResultsByTime']