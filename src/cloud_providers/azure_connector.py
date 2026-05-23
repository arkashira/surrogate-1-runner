from azure.identity import ClientSecretCredential
from azure.mgmt.costmanagement import CostManagementClient

class AzureConnector:
    def __init__(self, tenant_id, client_id, client_secret, subscription_id):
        self.credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )
        self.subscription_id = subscription_id
        self.client = CostManagementClient(self.credential, self.subscription_id)

    def get_costs(self, start_date, end_date):
        scope = f"/subscriptions/{self.subscription_id}"
        response = self.client.query.usage(
            scope=scope,
            parameters={
                "type": "Usage",
                "timeframe": "Custom",
                "timePeriod": {
                    "from": start_date,
                    "to": end_date
                },
                "dataset": {
                    "granularity": "Monthly",
                    "aggregation": {
                        "totalCost": {
                            "name": "PreTaxCost",
                            "function": "Sum"
                        }
                    }
                }
            }
        )
        return response