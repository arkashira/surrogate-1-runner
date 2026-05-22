import threading
from queue import Queue

class TerminalSync:
    def __init__(self):
        self.queue = Queue()
        self.lock = threading.Lock()

    def enqueue_change(self, change):
        with self.lock:
            self.queue.put(change)

    def process_changes(self):
        while True:
            change = self.queue.get()
            # Apply the change to the terminal state
            print(f"Processing change: {change}")
            self.queue.task_done()

    def start_sync(self):
        sync_thread = threading.Thread(target=self.process_changes, daemon=True)
        sync_thread.start()

# Example usage
if __name__ == "__main__":
    sync = TerminalSync()
    sync.enqueue_change("Change 1")
    sync.enqueue_change("Change 2")
    sync.start_sync()