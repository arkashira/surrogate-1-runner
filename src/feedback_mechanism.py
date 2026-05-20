import threading
import time

class FeedbackMechanism:
    def __init__(self):
        self.feedback_queue = []
        self.lock = threading.Lock()

    def add_feedback(self, message):
        with self.lock:
            self.feedback_queue.append(message)

    def get_feedback(self):
        with self.lock:
            return self.feedback_queue.pop(0) if self.feedback_queue else None

    def start_feedback_listener(self):
        def listen():
            while True:
                feedback = self.get_feedback()
                if feedback:
                    print(f"Real-time Feedback: {feedback}")
                time.sleep(1)

        listener_thread = threading.Thread(target=listen)
        listener_thread.daemon = True
        listener_thread.start()

# Example usage
if __name__ == "__main__":
    feedback = FeedbackMechanism()
    feedback.add_feedback("Proxy started successfully.")
    feedback.start_feedback_listener()