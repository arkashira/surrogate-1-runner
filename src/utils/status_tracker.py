import logging
import requests
import time

class StatusTracker:
    def __init__(self):
        self.ingestion_status = {}
        self.slack_webhook_url = "https://your-slack-webhook-url.com"

    def start_ingestion(self, shard_id):
        self.ingestion_status[shard_id] = {"started": time.time(), "progress": 0, "total": 0}

    def update_ingestion_status(self, shard_id, progress, total):
        self.ingestion_status[shard_id] = {"started": self.ingestion_status[shard_id]["started"], "progress": progress, "total": total}
        logging.info(f"Updated ingestion status for shard {shard_id}: {progress}/{total}")

    def finish_ingestion(self, shard_id):
        self.ingestion_status[shard_id] = {"finished": time.time(), "progress": 100, "total": 100}
        logging.info(f"Finished ingestion for shard {shard_id}")

    def report_failure(self, shard_id, error_message):
        logging.error(f"Error during ingestion for shard {shard_id}: {error_message}")
        self.send_slack_notification(f"Error during ingestion for shard {shard_id}: {error_message}")

    def send_slack_notification(self, message):
        requests.post(self.slack_webhook_url, json={"text": message})