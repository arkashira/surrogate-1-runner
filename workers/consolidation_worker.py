import time
import threading
from collections import defaultdict
from datetime import datetime, timedelta

class Alert:
    def __init__(self, service, message, timestamp):
        self.service = service
        self.message = message
        self.timestamp = timestamp

class ConsolidationWorker:
    def __init__(self):
        self.alerts = []
        self.lock = threading.Lock()
        self.consolidation_interval = 30  # seconds

    def ingest_alert(self, alert):
        with self.lock:
            self.alerts.append(alert)
            print(f"Alert ingested: {alert.service} - {alert.message} at {alert.timestamp}")

    def consolidate_alerts(self):
        while True:
            time.sleep(self.consolidation_interval)
            self._consolidate()

    def _consolidate(self):
        with self.lock:
            grouped_alerts = defaultdict(list)
            now = datetime.now()

            for alert in self.alerts:
                time_window_start = now - timedelta(minutes=5)
                if alert.timestamp >= time_window_start:
                    key = (alert.service, alert.message)
                    grouped_alerts[key].append(alert)

            self.alerts = []  # Clear alerts after consolidation
            for key, group in grouped_alerts.items():
                print(f"Consolidated alert: {key[0]} - {key[1]} | Count: {len(group)}")

if __name__ == "__main__":
    worker = ConsolidationWorker()
    threading.Thread(target=worker.consolidate_alerts, daemon=True).start()

    # Example usage
    worker.ingest_alert(Alert("serviceA", "Error occurred", datetime.now()))
    worker.ingest_alert(Alert("serviceA", "Error occurred", datetime.now()))
    worker.ingest_alert(Alert("serviceB", "Another error", datetime.now()))