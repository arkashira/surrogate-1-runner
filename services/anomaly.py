import datetime
import statistics
from typing import Dict, List

class BaselineCalculator:
    def __init__(self, data_service):
        self.data_service = data_service

    def calculate_baseline(self, resource_type: str, account_id: str) -> float:
        """
        Calculate the 7-day baseline for a given resource type and account.

        Args:
            resource_type: Type of resource (e.g., 'compute', 'storage')
            account_id: ID of the account

        Returns:
            The baseline value as a float
        """
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=7)

        data_points = self._get_data_points(resource_type, account_id, start_date, end_date)
        return statistics.mean(data_points)

    def _get_data_points(self, resource_type: str, account_id: str,
                         start_date: datetime.datetime, end_date: datetime.datetime) -> List[float]:
        """
        Retrieve data points for the given resource type, account, and date range.

        Args:
            resource_type: Type of resource
            account_id: ID of the account
            start_date: Start date for the range
            end_date: End date for the range

        Returns:
            List of data points as floats
        """
        query = {
            "resource_type": resource_type,
            "account_id": account_id,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }

        return self.data_service.query_data_points(query)

class DataService:
    def query_data_points(self, query: Dict) -> List[float]:
        """
        Query data points from the data service.

        Args:
            query: Dictionary containing query parameters

        Returns:
            List of data points as floats
        """
        # Implementation would connect to actual data source
        # This is a mock implementation for demonstration
        return [100.0, 105.0, 110.0, 108.0, 112.0, 107.0, 115.0]