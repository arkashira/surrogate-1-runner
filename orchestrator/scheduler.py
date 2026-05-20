import heapq
import time
from typing import Dict, List, Tuple, Callable
from prometheus_client import Counter, Gauge

class PriorityTaskScheduler:
    def __init__(self):
        self.task_queue: List[Tuple[float, int, Callable]] = []
        self.task_counter = Counter('tasks_total', 'Total tasks processed')
        self.queue_depth = Gauge('task_queue_depth', 'Current task queue depth')

    def add_task(self, task: Callable, priority: float) -> None:
        """Add a task to the priority queue."""
        task_id = int(time.time() * 1000)  # 1ms resolution
        heapq.heappush(self.task_queue, (priority, task_id, task))
        self.queue_depth.inc()

    def execute_tasks(self) -> None:
        """Execute tasks from the priority queue."""
        while self.task_queue:
            priority, task_id, task = heapq.heappop(self.task_queue)
            self.queue_depth.dec()
            try:
                task()
                self.task_counter.inc()
            except Exception as e:
                print(f"Task execution failed: {e}")

    def run(self) -> None:
        """Run the scheduler in a loop."""
        while True:
            self.execute_tasks()
            time.sleep(0.0001)  # 0.1ms resolution

class Task:
    def __init__(self, func: Callable, args: tuple = (), kwargs: dict = None):
        self.func = func
        self.args = args
        self.kwargs = kwargs or {}

    def __call__(self):
        return self.func(*self.args, **self.kwargs)

def create_task(func: Callable, *args, **kwargs) -> Task:
    """Create a task with the given function and arguments."""
    return Task(func, args, kwargs)