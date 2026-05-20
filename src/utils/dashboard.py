import logging
from utils.status_tracker import StatusTracker

class Dashboard:
    def __init__(self):
        self.status_tracker = StatusTracker()

    def get_ingestion_queue_length(self):
        return len(self.status_tracker.ingestion_status)

    def get_success_rates(self):
        success_count = 0
        for shard_id, status in self.status_tracker.ingestion_status.items():
            if "finished" in status:
                success_count += 1
        return success_count / len(self.status_tracker.ingestion_status)

    def update_dashboard(self):
        logging.info(f"Ingestion queue length: {self.get_ingestion_queue_length()}")
        logging.info(f"Success rates: {self.get_success_rates()}")