import requests
from datetime import datetime

class AnomalyDetector:
    def __init__(self):
        self.metrics_url = "http://metrics-service/api/anomalies"

    def report_anomaly(self, entity_type, entity_name, namespace, reason):
        anomaly_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "entity_type": entity_type,
            "entity_name": entity_name,
            "namespace": namespace,
            "reason": reason
        }
        try:
            response = requests.post(self.metrics_url, json=anomaly_data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to report anomaly: {e}")