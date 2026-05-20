import time
import threading
from collections import defaultdict
from flask import Flask, jsonify

app = Flask(__name__)

class MetricsAggregator:
    def __init__(self):
        self.total_alerts = 0
        self.consolidated_alerts = 0
        self.noise_alerts = 0
        self.lock = threading.Lock()
        self.reduction_percentage = 0.0

    def process_alert(self, alert):
        with self.lock:
            self.total_alerts += 1
            if alert['is_noise']:
                self.noise_alerts += 1
            else:
                self.consolidated_alerts += 1
            self.update_reduction_percentage()

    def update_reduction_percentage(self):
        if self.total_alerts > 0:
            self.reduction_percentage = (self.noise_alerts / self.total_alerts) * 100

    def get_metrics(self):
        with self.lock:
            return {
                'total_alerts': self.total_alerts,
                'consolidated_alerts': self.consolidated_alerts,
                'noise_alerts': self.noise_alerts,
                'reduction_percentage': self.reduction_percentage
            }

metrics_aggregator = MetricsAggregator()

@app.route('/metrics', methods=['GET'])
def metrics():
    return jsonify(metrics_aggregator.get_metrics())

def alert_listener():
    while True:
        # Simulate receiving alerts
        time.sleep(1)  # Replace with actual alert receiving logic
        alert = {'is_noise': False}  # Replace with actual alert data
        metrics_aggregator.process_alert(alert)

if __name__ == '__main__':
    threading.Thread(target=alert_listener, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)