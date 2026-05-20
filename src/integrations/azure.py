import os
import logging
from datetime import datetime, timedelta
from azure.identity import ClientSecretCredential
from azure.mgmt.costmanagement import CostManagementClient
from azure.core.exceptions import HttpResponseError, ClientAuthenticationError

logger = logging.getLogger(__name__)

class AzureCostIntegration:
    def __init__(self, subscription_id, tenant_id, client_id, client_secret):
        self.subscription_id = subscription_id
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.client = None
        self._authenticate()

    def _authenticate(self):
        try:
            credential = ClientSecretCredential(
                tenant_id=self.tenant_id,
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            self.client = CostManagementClient(credential)
            logger.info("Successfully authenticated with Azure")
        except ClientAuthenticationError as e:
            logger.error(f"Azure authentication failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during Azure authentication: {str(e)}")
            raise

    def get_cost_data(self, start_date, end_date):
        try:
            query = {
                "type": "ActualCost",
                "timeframe": "Custom",
                "timePeriod": {
                    "from": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "to": end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
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

            result = self.client.query.usage(
                self.subscription_id,
                query
            )
            
            if result.value:
                return [{
                    "date": row.time_period.from_date,
                    "cost": row.total_cost
                } for row in result.value]
            return []
            
        except HttpResponseError as e:
            logger.error(f"Azure cost data retrieval failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during Azure cost retrieval: {str(e)}")
            raise

    def test_connection(self):
        try:
            # Test with a minimal query to validate credentials
            test_start = datetime.utcnow() - timedelta(days=1)
            test_end = datetime.utcnow()
            self.get_cost_data(test_start, test_end)
            return True
        except Exception as e:
            logger.error(f"Azure connection test failed: {str(e)}")
            return False