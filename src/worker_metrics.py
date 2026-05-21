from prometheus_client import start_http_server, Gauge
import time

class WorkerMetrics:
    def __init__(self, port=8000):
        self.port = port
        self.worker_status = Gauge('worker_status', 'Status of the worker', ['worker_id'])
        self.dataset_size = Gauge('dataset_size', 'Size of the dataset being processed', ['worker_id'])

    def start_metrics_server(self):
        start_http_server(self.port)

    def update_worker_status(self, worker_id, status):
        self.worker_status.labels(worker_id=worker_id).set(status)

    def update_dataset_size(self, worker_id, size):
        self.dataset_size.labels(worker_id=worker_id).set(size)

# Example usage
if __name__ == "__main__":
    metrics = WorkerMetrics()
    metrics.start_metrics_server()
    while True:
        # Update metrics here
        time.sleep(1)