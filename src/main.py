import os
from worker import Worker

if __name__ == "__main__":
    worker_id = os.getenv('WORKER_ID', 'worker1')
    dataset_size = int(os.getenv('DATASET_SIZE', 1000))
    worker = Worker(worker_id, dataset_size)
    worker.start()
    worker.run()