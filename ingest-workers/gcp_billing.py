import time
import logging
from typing import List, Dict, Any
from google.cloud import billing_v1
from google.api_core import retry
from google.cloud.exceptions import GoogleCloudError
import backoff

logger = logging.getLogger(__name__)

class GCPBillingClient:
    def __init__(self, billing_account_id: str):
        self.billing_account_id = billing_account_id
        self.client = billing_v1.CloudBillingClient()

    @backoff.on_exception(
        backoff.expo,
        (GoogleCloudError, Exception),
        max_tries=5,
        factor=2,
        jitter=backoff.full_jitter
    )
    def fetch_billing_data(self) -> List[Dict[str, Any]]:
        """
        Fetch billing data from GCP Billing API.

        Returns:
            List of billing records.
        """
        try:
            logger.info("Fetching billing accounts...")
            billing_accounts = self.client.list_billing_accounts()
            billing_account = next((account for account in billing_accounts if account.open_), None)

            if not billing_account:
                raise Exception("No open billing account found")

            logger.info(f"Using billing account: {billing_account.name}")
            request = billing_v1.ListProjectBillingInfoRequest(name=billing_account.name)
            projects = [project_info.project_id for project_info in self.client.list_project_billing_info(request=request)]

            if not projects:
                logger.warning("No projects found in billing account")
                return []

            # Fetch usage data for the first project
            project_id = projects[0]
            logger.info(f"Fetching billing data for project {project_id}")

            # Simulate API call delay
            time.sleep(0.1)

            # Return mock data structure (replace with actual API call)
            return [{
                "project_id": project_id,
                "cost": 100.0,
                "usage": "compute",
                "timestamp": time.time(),
                "currency": "USD"
            }]
        except Exception as e:
            logger.error(f"Error fetching billing data: {str(e)}")
            return []

    def ingest_cost_data(self) -> int:
        """
        Ingest cost data with retry logic and latency monitoring.

        Returns:
            Number of records ingested.
        """
        start_time_ns = time.perf_counter_ns()
        records = self.fetch_billing_data()

        # Simulate storing records (in real implementation, this would be database storage)
        time.sleep(0.05)  # Simulate storage latency

        end_time_ns = time.perf_counter_ns()
        latency_ms = (end_time_ns - start_time_ns) / 1_000_000

        if latency_ms > 30:
            logger.warning(f"High ingestion latency detected: {latency_ms:.2f}ms")

        logger.info(f"Ingested {len(records)} records with {latency_ms:.2f}ms latency")
        return len(records)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    client = GCPBillingClient("your_billing_account_id")
    while True:
        client.ingest_cost_data()
        time.sleep(300)  # Wait for 5 minutes before the next fetch