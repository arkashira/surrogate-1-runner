import time
import random
from prometheus_client import start_http_server, Gauge
from queue import PriorityQueue

# Metrics
TASK_QUEUE_DEPTH = Gauge('task_queue_depth', 'Current depth of the task queue')
TASK_LATENCY = Gauge('task_latency_seconds', 'Latency of task execution in seconds')

class Task:
    def __init__(self, priority, task_id):
        self.priority = priority
        self.task_id = task_id
        self.creation_time = time.time()

    def __lt__(self, other):
        return self.priority < other.priority

def execute_task(task):
    # Simulate task execution time
    time.sleep(random.uniform(0.0001, 0.001))
    latency = time.time() - task.creation_time
    TASK_LATENCY.set(latency)
    return latency

def run_benchmark(num_tasks):
    task_queue = PriorityQueue()
    latencies = []

    # Start Prometheus metrics server
    start_http_server(8000)

    # Add tasks to the queue
    for i in range(num_tasks):
        priority = random.uniform(0, 1)
        task = Task(priority, i)
        task_queue.put(task)
        TASK_QUEUE_DEPTH.set(task_queue.qsize())

    # Execute tasks
    while not task_queue.empty():
        task = task_queue.get()
        latency = execute_task(task)
        latencies.append(latency)
        TASK_QUEUE_DEPTH.set(task_queue.qsize())

    # Calculate average latency
    average_latency = sum(latencies) / len(latencies)
    print(f"Average latency: {average_latency} seconds")

if __name__ == "__main__":
    run_benchmark(10000)