import threading
import time
import json

class RealTimeCollaboration:
    def __init__(self):
        self.lock = threading.Lock()
        self.tasks = {}
        self.updates = []

    def start(self):
        threading.Thread(target=self.update_loop).start()

    def update_loop(self):
        while True:
            with self.lock:
                for task_id, task in self.tasks.items():
                    self.updates.append({"task_id": task_id, "task": task})
            time.sleep(1)

    def update_task(self, task):
        with self.lock:
            task_id = task["id"]
            self.tasks[task_id] = task

    def stop(self):
        pass

    def get_updates(self):
        with self.lock:
            updates = self.updates[:]
            self.updates = []
            return updates