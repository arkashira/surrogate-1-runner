from azure.mgmt.costmanagement import CostManagementClient
from azure.identity import DefaultAzureCredential
from datetime import datetime, timedelta

class AzureCostManagement:
    def __init__(self, subscription_id):
        self.credential = DefaultAzureCredential()
        self.client = CostManagementClient(credential=self.credential, subscription_id=subscription_id)

    def get_real_time_cost(self, start_date=None, end_date=None):
        if not start_date:
            start_date = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.utcnow().strftime('%Y-%m-%d')

        query = self.client.query.create(
            scope=f"/subscriptions/{self.subscription_id}",
            parameters={
                "type": "Usage",
                "timeframe": "Custom",
                "time_period": {
                    "from": start_date,
                    "to": end_date
                },
                "dataset": {
                    "granularity": "Daily",
                    "aggregation": {
                        "totalCost": {
                            "name": "PreTaxCost",
                            "function": "Sum"
                        }
                    }
                }
            }
        )
        return query.properties.rows

    def filter_cost_by_resource_type(self, resource_type, start_date=None, end_date=None):
        query = self.client.query.create(
            scope=f"/subscriptions/{self.subscription_id}",
            parameters={
                "type": "Usage",
                "timeframe": "Custom",
                "time_period": {
                    "from": start_date,
                    "to": end_date
                },
                "dataset": {
                    "granularity": "Daily",
                    "aggregation": {
                        "totalCost": {
                            "name": "PreTaxCost",
                            "function": "Sum"
                        }
                    },
                    "filter": {
                        "and": [
                            {
                                "dimensions": {
                                    "name": "ResourceType",
                                    "operator": "In",
                                    "values": [resource_type]
                                }
                            }
                        ]
                    }
                }
            }
        )
        return query.properties.rows

    def filter_cost_by_location(self, location, start_date=None, end_date=None):
        query = self.client.query.create(
            scope=f"/subscriptions/{self.subscription_id}",
            parameters={
                "type": "Usage",
                "timeframe": "Custom",
                "time_period": {
                    "from": start_date,
                    "to": end_date
                },
                "dataset": {
                    "granularity": "Daily",
                    "aggregation": {
                        "totalCost": {
                            "name": "PreTaxCost",
                            "function": "Sum"
                        }
                    },
                    "filter": {
                        "and": [
                            {
                                "dimensions": {
                                    "name": "ResourceLocation",
                                    "operator": "In",
                                    "values": [location]
                                }
                            }
                        ]
                    }
                }
            }
        )
        return query.properties.rows