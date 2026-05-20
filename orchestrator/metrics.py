from prometheus_client import start_http_server, Counter, Gauge

class Metrics:
    def __init__(self, port=8000):
        self.port = port
        self.task_counter = Counter('tasks_total', 'Total tasks processed')
        self.queue_depth = Gauge('task_queue_depth', 'Current task queue depth')

    def start(self):
        """Start the Prometheus metrics server."""
        start_http_server(self.port)

    def increment_task_counter(self):
        """Increment the task counter."""
        self.task_counter.inc()

    def set_queue_depth(self, depth: int):
        """Set the current task queue depth."""
        self.queue_depth.set(depth)