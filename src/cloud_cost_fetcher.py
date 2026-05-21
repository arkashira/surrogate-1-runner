import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class CloudCostFetcher:
    def __init__(self, api_key: str, cloud_provider: str):
        self.api_key = api_key
        self.cloud_provider = cloud_provider
        self.base_url = self._get_base_url()

    def _get_base_url(self) -> str:
        if self.cloud_provider.lower() == 'aws':
            return 'https://awscostexplorer.amazonaws.com/'
        elif self.cloud_provider.lower() == 'azure':
            return 'https://management.azure.com/'
        elif self.cloud_provider.lower() == 'gcp':
            return 'https://cloudbilling.googleapis.com/'
        else:
            raise ValueError(f"Unsupported cloud provider: {self.cloud_provider}")

    def _get_headers(self) -> Dict[str, str]:
        if self.cloud_provider.lower() == 'aws':
            return {
                'Content-Type': 'application/json',
                'x-amz-security-token': self.api_key
            }
        elif self.cloud_provider.lower() == 'azure':
            return {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }
        elif self.cloud_provider.lower() == 'gcp':
            return {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }

    def _get_time_range(self, time_range: str) -> Dict[str, str]:
        end_time = datetime.utcnow()
        if time_range == 'last_hour':
            start_time = end_time - timedelta(hours=1)
        elif time_range == 'last_day':
            start_time = end_time - timedelta(days=1)
        elif time_range == 'last_week':
            start_time = end_time - timedelta(weeks=1)
        elif time_range == 'last_month':
            start_time = end_time - timedelta(days=30)
        else:
            raise ValueError(f"Unsupported time range: {time_range}")

        return {
            'Start': start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'End': end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        }

    def fetch_cost_data(self, time_range: str, service: Optional[str] = None) -> List[Dict]:
        time_range_params = self._get_time_range(time_range)
        headers = self._get_headers()

        if self.cloud_provider.lower() == 'aws':
            payload = {
                'TimePeriod': time_range_params,
                'Granularity': 'HOURLY',
                'Metrics': ['UnblendedCost']
            }
            if service:
                payload['Filter'] = {
                    'Dimensions': {
                        'Key': 'SERVICE',
                        'Values': [service]
                    }
                }
            response = requests.post(
                f'{self.base_url}GetCostAndUsage',
                headers=headers,
                data=json.dumps(payload)
            )
        elif self.cloud_provider.lower() == 'azure':
            payload = {
                'timeframe': 'Custom',
                'timePeriod': time_range_params,
                'type': 'Usage',
                'dataSet': {
                    'granularity': 'Daily',
                    'aggregation': {
                        'totalCost': {
                            'name': 'PreTaxCost',
                            'function': 'Sum'
                        }
                    }
                }
            }
            if service:
                payload['filter'] = {
                    'dimensions': {
                        'name': 'ResourceType',
                        'operator': 'In',
                        'values': [service]
                    }
                }
            response = requests.post(
                f'{self.base_url}subscriptions/{self.api_key}/providers/Microsoft.CostManagement/query',
                headers=headers,
                data=json.dumps(payload)
            )
        elif self.cloud_provider.lower() == 'gcp':
            payload = {
                'timeRange': time_range_params,
                'aggregations': [
                    {
                        'aggregation': {
                            'aggregationCount': {
                                'aggregationCount': 'COUNT'
                            }
                        }
                    }
                ]
            }
            if service:
                payload['filter'] = {
                    'service': service
                }
            response = requests.post(
                f'{self.base_url}v1/projects/{self.api_key}/services/{service}/cost',
                headers=headers,
                data=json.dumps(payload)
            )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch cost data: {response.text}")