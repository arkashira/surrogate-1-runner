import os
import time
from worker_metrics import WorkerMetrics

class Worker:
    def __init__(self, worker_id, dataset_size):
        self.worker_id = worker_id
        self.dataset_size = dataset_size
        self.metrics = WorkerMetrics()

    def start(self):
        self.metrics.start_metrics_server()
        self.metrics.update_worker_status(self.worker_id, 1)
        self.metrics.update_dataset_size(self.worker_id, self.dataset_size)
        print(f"Worker {self.worker_id} started with dataset size {self.dataset_size}")

    def run(self):
        while True:
            # Simulate work
            time.sleep(1)

if __name__ == "__main__":
    worker_id = os.getenv('WORKER_ID', 'worker1')
    dataset_size = int(os.getenv('DATASET_SIZE', 1000))
    worker = Worker(worker_id, dataset_size)
    worker.start()
    worker.run()