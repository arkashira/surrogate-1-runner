from google.cloud import bigquery

class GCPConnector:
    def __init__(self, project_id, credentials_path):
        self.client = bigquery.Client.from_service_account_json(credentials_path)
        self.project_id = project_id

    def get_costs(self, start_date, end_date):
        query = f"""
            SELECT
                service.description AS service,
                sku.description AS sku,
                cost
            FROM `{self.project_id}.gcp_billing_export_v1_012345_678901_2023`
            WHERE usage_start_time BETWEEN '{start_date}' AND '{end_date}'
        """
        query_job = self.client.query(query)
        results = query_job.result()
        return [dict(row) for row in results]