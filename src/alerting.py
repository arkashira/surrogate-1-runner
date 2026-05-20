import time
import random
import logging
from prometheus_client import Gauge, start_http_server

# Define metrics
node_cpu_usage = Gauge('node_cpu_usage', 'CPU usage of the node')
node_memory_usage = Gauge('node_memory_usage', 'Memory usage of the node')
node_disk_usage = Gauge('node_disk_usage', 'Disk usage of the node')

class AlertingSystem:
    def __init__(self, threshold=0.8):
        self.threshold = threshold
        self.metrics = []

    def collect_metrics(self):
        # Simulate collecting metrics from nodes
        for _ in range(10):  # Simulate 10 nodes
            metric = random.uniform(0, 1)  # Random metric value between 0 and 1
            self.metrics.append(metric)
            logging.info(f"Collected metric: {metric}")
            # Update Prometheus metrics
            node_cpu_usage.set(metric)  # Example for CPU usage

    def analyze_metrics(self):
        if not self.metrics:
            logging.warning("No metrics to analyze.")
            return

        average = sum(self.metrics) / len(self.metrics)
        logging.info(f"Average metric value: {average}")

        if average > self.threshold:
            self.raise_alert(average)

    def raise_alert(self, average):
        logging.error(f"Alert! Average metric {average} exceeds threshold {self.threshold}.")

    def run(self):
        # Start Prometheus metrics server
        start_http_server(8000)
        while True:
            self.collect_metrics()
            self.analyze_metrics()
            time.sleep(60)  # Collect metrics every minute

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    alerting_system = AlertingSystem()
    alerting_system.run()