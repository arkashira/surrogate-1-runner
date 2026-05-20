import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
from google.cloud import billing

@dataclass
class CostItem:
    """
    Represents a single line-item cost record.

    Attributes
    ----------
    provider : str
        Cloud provider name (e.g., "gcp").
    service : str
        Service name (e.g., "Compute Engine").
    region : str
        Region identifier (e.g., "us-east1").
    usage_type : str
        Specific usage type or SKU (e.g., "n1-standard-1").
    cost : float
        Monetary cost in the provider's default currency.
    currency : str
        Currency code (e.g., "USD").
    timestamp : datetime
        The time period the cost applies to (start of the period).
    metadata : Dict[str, Any] = field(default_factory=dict)
        Optional provider-specific metadata.
    """

    provider: str
    service: str
    region: str
    usage_type: str
    cost: float
    currency: str
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Return a serialisable dictionary representation."""
        return {
            "provider": self.provider,
            "service": self.service,
            "region": self.region,
            "usage_type": self.usage_type,
            "cost": self.cost,
            "currency": self.currency,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


class GcpCostFetcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://cloudbilling.googleapis.com/v1/"

    def fetch_cost_data(self) -> List[CostItem]:
        """
        Fetches cost data from GCP for the last 24 hours or on demand.
        Returns a list of CostItem objects.
        """
        now = datetime.utcnow()
        start_time = (now - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        end_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Try to use the google-cloud-billing library
        try:
            billing_client = billing.BillingClient()
            billing_instance = billing_client.get_billing_instance()
            cost_client = billing_client.get_cost_client()
            cost_data = cost_client.get_cost(
                billing_instance=billing_instance,
                start_time=start_time,
                end_time=end_time,
            )
            cost_items = self._process_cost_data(cost_data)
            return cost_items
        except Exception as e:
            # Fall back to the REST API
            print(f"Error using google-cloud-billing library: {e}")
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            cost_data_list = []
            services = self._get_services()
            for service in services:
                for region in self._get_regions(service):
                    cost_data = self._fetch_service_region_cost(service, region, start_time, end_time)
                    if cost_data:
                        cost_items = self._process_cost_data(cost_data)
                        cost_data_list.extend(cost_items)
            return cost_data_list

    def _get_services(self) -> List[str]:
        """
        Fetches the list of services available in GCP.
        """
        url = f"{self.base_url}services"
        response = requests.get(url, headers={"Authorization": f"Bearer {self.api_key}"})
        response.raise_for_status()
        services = [service["name"] for service in response.json().get("services", [])]
        return services

    def _get_regions(self, service: str) -> List[str]:
        """
        Fetches the list of regions available for a given service in GCP.
        """
        url = f"{self.base_url}services/{service}/locations"
        response = requests.get(url, headers={"Authorization": f"Bearer {self.api_key}"})
        response.raise_for_status()
        regions = [location["name"] for location in response.json().get("locations", [])]
        return regions

    def _fetch_service_region_cost(self, service: str, region: str, start_time: str, end_time: str) -> Dict:
        """
        Fetches cost data for a specific service and region in GCP.
        """
        url = f"{self.base_url}services/{service}/locations/{region}/costs"
        params = {
            "startTime": start_time,
            "endTime": end_time
        }
        response = requests.get(url, headers={"Authorization": f"Bearer {self.api_key}"}, params=params)
        response.raise_for_status()
        cost_data = response.json()

        return cost_data

    def _process_cost_data(self, cost_data: Dict) -> List[CostItem]:
        """
        Process the cost data and create a list of CostItem objects.
        """
        cost_items = []
        for item in cost_data.get("costs", []):
            cost_items.append(CostItem(
                provider="gcp",
                service=item.get("service", ""),
                region=item.get("region", ""),
                usage_type=item.get("usageType", ""),
                cost=item.get("cost", 0.0),
                currency=item.get("currency", "USD"),
                timestamp=datetime.fromisoformat(item.get("startTime")),
                metadata=item.get("metadata", {}),
            ))
        return cost_items