import boto3
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class AWSCostExplorerClient:
    def __init__(self, access_key: str, secret_key: str, region: str = 'us-east-1'):
        self.client = boto3.client(
            'ce',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        self.logger = logging.getLogger(__name__)

    def get_cost_and_usage(
        self,
        start_date: str,
        end_date: str,
        granularity: str = 'DAILY',
        metrics: List[str] = ['UnblendedCost', 'UsageQuantity'],
        group_by: Optional[List[Dict]] = None
    ) -> List[Dict]:
        """
        Fetch cost and usage data from AWS Cost Explorer API.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            granularity: Granularity of the data (DAILY, MONTHLY, etc.)
            metrics: List of metrics to retrieve
            group_by: List of dictionaries specifying how to group the data

        Returns:
            List of dictionaries containing cost and usage data
        """
        try:
            response = self.client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date,
                    'End': end_date
                },
                Granularity=granularity,
                Metrics=metrics,
                GroupBy=group_by if group_by else []
            )
            return response.get('ResultsByTime', [])
        except Exception as e:
            self.logger.error(f"Error fetching cost and usage data: {str(e)}")
            return []

    def get_daily_cost_data(self, days: int = 1) -> List[Dict]:
        """
        Fetch daily cost data for the last N days.

        Args:
            days: Number of days to look back

        Returns:
            List of dictionaries containing daily cost data
        """
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        group_by = [
            {
                'Type': 'DIMENSION',
                'Key': 'SERVICE'
            },
            {
                'Type': 'DIMENSION',
                'Key': 'LINKED_ACCOUNT'
            }
        ]

        return self.get_cost_and_usage(
            start_date=start_date,
            end_date=end_date,
            granularity='DAILY',
            group_by=group_by
        )