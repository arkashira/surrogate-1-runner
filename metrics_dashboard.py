import logging
from ingest_worker import IngestionWorker

class MetricsDashboard:
    def __init__(self):
        self.worker = IngestionWorker()
        self.logger = logging.getLogger(__name__)

    def display_metrics(self) -> None:
        avg_latencies = self.worker.get_average_latency_per_dataset()

        self.logger.info("Average processing time per dataset:")
        for dataset, avg_time in avg_latencies.items():
            self.logger.info(f"{dataset}: {avg_time:.2f} seconds")

if __name__ == "__main__":
    dashboard = MetricsDashboard()
    dashboard.display_metrics()