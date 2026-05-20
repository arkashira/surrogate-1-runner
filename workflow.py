import os
import threading
from queue import Queue
from collab import RealTimeCollaboration

class WorkflowManager:
    def __init__(self):
        self.collab = RealTimeCollaboration()
        self.queue = Queue()

    def start(self):
        threading.Thread(target=self.collab.start).start()
        self.process_queue()

    def process_queue(self):
        while True:
            task = self.queue.get()
            if task is None:
                break
            self.collab.update_task(task)

    def add_task(self, task):
        self.queue.put(task)

    def stop(self):
        self.queue.put(None)
        self.collab.stop()

def main():
    workflow = WorkflowManager()
    workflow.start()

if __name__ == "__main__":
    main()