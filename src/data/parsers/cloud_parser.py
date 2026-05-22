import json
from typing import Dict, List, Optional
from src.models.cloud_provider import CloudProvider, AWS, GCP, Azure

class CloudCostParser:
    def __init__(self):
        self.providers = {
            'aws': AWS(),
            'gcp': GCP(),
            'azure': Azure()
        }

    def parse_cost_data(self, provider: str, data: str) -> List[Dict]:
        """
        Parse cost data from a given cloud provider.

        Args:
            provider: The cloud provider (aws, gcp, azure)
            data: The cost data in JSON format

        Returns:
            List of parsed cost data with a consistent schema
        """
        try:
            cost_data = json.loads(data)
            return self.providers[provider].parse(cost_data)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON data")
        except KeyError:
            raise ValueError(f"Unsupported provider: {provider}")

    def aggregate_costs(self, costs: List[Dict]) -> Dict:
        """
        Aggregate costs across multiple cloud providers.

        Args:
            costs: List of cost data from different providers

        Returns:
            Aggregated cost data
        """
        aggregated = {
            'total_cost': 0.0,
            'cost_by_provider': {},
            'cost_by_service': {},
            'time_period': None
        }

        for cost in costs:
            if not cost:
                continue

            provider = cost.get('provider', 'unknown')
            amount = cost.get('amount', 0.0)
            service = cost.get('service', 'unknown')
            start_time = cost.get('start_time')
            end_time = cost.get('end_time')

            # Update total cost
            aggregated['total_cost'] += amount

            # Update cost by provider
            if provider not in aggregated['cost_by_provider']:
                aggregated['cost_by_provider'][provider] = 0.0
            aggregated['cost_by_provider'][provider] += amount

            # Update cost by service
            if service not in aggregated['cost_by_service']:
                aggregated['cost_by_service'][service] = 0.0
            aggregated['cost_by_service'][service] += amount

            # Set time period
            if not aggregated['time_period']:
                if start_time and end_time:
                    aggregated['time_period'] = {
                        'start_time': start_time,
                        'end_time': end_time
                    }

        return aggregated