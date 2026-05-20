import yaml
import requests
import logging
from datetime import datetime

class AnomalyDetector:
    def __init__(self, config_path='/opt/axentx/surrogate-1/surrogate-1.yaml'):
        self.config = self._load_config(config_path)
        self.slack_webhook_url = self.config.get('slack_webhook_url')
        self.logger = logging.getLogger(__name__)

    def _load_config(self, config_path):
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def detect_anomalies(self, data):
        # Placeholder for anomaly detection logic
        anomalies = []
        for item in data:
            if item['severity'] == 'HIGH':
                anomalies.append(item)
        return anomalies

    def notify_slack(self, anomaly):
        if anomaly['severity'] != 'HIGH':
            self.logger.info(f"LOW severity anomaly logged: {anomaly}")
            return

        payload = {
            "provider": anomaly.get('provider'),
            "service": anomaly.get('service'),
            "observed_spend": anomaly.get('observed_spend'),
            "threshold_breach": anomaly.get('threshold_breach')
        }

        response = requests.post(self.slack_webhook_url, json=payload)
        if response.status_code != 200:
            self.logger.error(f"Failed to send Slack alert: {response.text}")

    def process_data(self, data):
        anomalies = self.detect_anomalies(data)
        for anomaly in anomalies:
            self.notify_slack(anomaly)

# Example usage
if __name__ == "__main__":
    detector = AnomalyDetector()
    sample_data = [
        {"severity": "HIGH", "provider": "AWS", "service": "EC2", "observed_spend": 1000, "threshold_breach": True},
        {"severity": "LOW", "provider": "GCP", "service": "Compute Engine", "observed_spend": 500, "threshold_breach": False}
    ]
    detector.process_data(sample_data)