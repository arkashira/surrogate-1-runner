import os
import logging
from datetime import datetime, timedelta
from azure.mgmt.consumption import ConsumptionManagementClient
from azure.identity import DefaultAzureCredential

logging.basicConfig(filename='/var/log/surrogate-cost-ingest.log', level=logging.INFO)

class AzureCostClient:
    def __init__(self):
        self.credential = DefaultAzureCredential()
        self.subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
        if not self.subscription_id:
            raise ValueError("AZURE_SUBSCRIPTION_ID environment variable is not set.")
        self.client = ConsumptionManagementClient(self.credential, self.subscription_id)

    def fetch_costs(self, start_date=None, end_date=None):
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')

        try:
            costs = self.client.usage_details.list(billing_period_name='Current', expand='properties/meterDetails')
            return [self._normalize_cost(cost, start_date, end_date) for cost in costs]
        except Exception as e:
            logging.error(f"Failed to fetch Azure costs: {str(e)}")
            raise

    def _normalize_cost(self, cost, start_date, end_date):
        normalized_cost = {
            'provider': 'azure',
            'billing_period_start_date': start_date,
            'billing_period_end_date': end_date,
            'cost': cost.properties.pre_tax_cost,
            'currency': cost.properties.currency,
            'resource_id': cost.properties.resource_id,
            'usage_start_date': cost.properties.usage_start_date.strftime('%Y-%m-%d'),
            'usage_end_date': cost.properties.usage_end_date.strftime('%Y-%m-%d'),
            'meter_id': cost.properties.meter_id,
            'meter_name': cost.properties.meter_name,
            'meter_category': cost.properties.meter_category,
            'meter_subcategory': cost.properties.meter_subcategory,
            'unit_of_measure': cost.properties.unit_of_measure,
            'instance_id': cost.properties.instance_id,
            'tags': cost.properties.tags
        }
        return normalized_cost

    def save_costs(self, costs):
        today = datetime.now().strftime('%Y/%m/%d')
        file_path = f'/data/costs/{today}.json'
        with open(file_path, 'w') as f:
            json.dump(costs, f, indent=4)
        logging.info(f"Azure costs saved to {file_path}")

if __name__ == "__main__":
    client = AzureCostClient()
    try:
        costs = client.fetch_costs()
        client.save_costs(costs)
        logging.info("Azure cost ingestion completed successfully.")
    except Exception as e:
        logging.error(f"Azure cost ingestion failed: {str(e)}")