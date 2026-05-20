import time
import logging
from utils.status_tracker import StatusTracker

class IngestionWorker:
    def __init__(self, shard_id, dataset):
        self.shard_id = shard_id
        self.dataset = dataset
        self.status_tracker = StatusTracker()

    def ingest(self):
        logging.info(f"Starting ingestion for shard {self.shard_id}")
        self.status_tracker.start_ingestion(self.shard_id)
        try:
            # Ingestion logic here
            for i in range(100):
                logging.info(f"Ingesting {i+1} of 100")
                self.status_tracker.update_ingestion_status(self.shard_id, i+1, 100)
                time.sleep(0.5)
            self.status_tracker.finish_ingestion(self.shard_id)
        except Exception as e:
            logging.error(f"Error during ingestion: {e}")
            self.status_tracker.report_failure(self.shard_id, str(e))

    def run(self):
        while True:
            self.ingest()
            time.sleep(30)