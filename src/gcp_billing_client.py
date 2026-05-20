import os
from google.cloud import bigquery
from google.oauth2 import service_account

class GCPBillingClient:
    def __init__(self):
        self.credentials = service_account.Credentials.from_service_account_file(
            os.getenv('GCP_SERVICE_ACCOUNT_FILE')
        )
        self.client = bigquery.Client(credentials=self.credentials, project=os.getenv('GCP_PROJECT_ID'))

    def fetch_cost_data(self, project_id=None, resource_type=None):
        query = """
            SELECT
                project.id AS project_id,
                service.description AS resource_type,
                cost,
                currency,
                usage_start_time,
                usage_end_time
            FROM
                `project_id.dataset_id.gcp_billing_export_v1`
            WHERE
                _PARTITIONTIME BETWEEN TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), DAY, 'UTC')
                AND TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), DAY, 'UTC') + INTERVAL 1 DAY
        """

        if project_id:
            query += f" AND project.id = '{project_id}'"
        if resource_type:
            query += f" AND service.description = '{resource_type}'"

        query_job = self.client.query(query)
        results = query_job.result()

        cost_data = []
        for row in results:
            cost_data.append({
                'project_id': row.project_id,
                'resource_type': row.resource_type,
                'cost': row.cost,
                'currency': row.currency,
                'usage_start_time': row.usage_start_time,
                'usage_end_time': row.usage_end_time
            })

        return cost_data