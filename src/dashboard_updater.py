import time
from typing import Dict, List, Optional
from cloud_cost_fetcher import CloudCostFetcher

class DashboardUpdater:
    def __init__(self, api_key: str, cloud_provider: str):
        self.cloud_cost_fetcher = CloudCostFetcher(api_key, cloud_provider)

    def update_dashboard(self, time_range: str, service: Optional[str] = None) -> None:
        while True:
            cost_data = self.cloud_cost_fetcher.fetch_cost_data(time_range, service)
            self._display_cost_data(cost_data)
            time.sleep(300)  # Update every 5 minutes

    def _display_cost_data(self, cost_data: List[Dict]) -> None:
        print("Real-time Cost Data:")
        for data in cost_data:
            print(f"Time: {data['timePeriod']['start']} to {data['timePeriod']['end']}")
            print(f"Total Cost: {data['total']['unblendedCost']['amount']} {data['total']['unblendedCost']['unit']}")
            print("---")