import threading
from typing import Dict, List

class TerminalSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.users: Dict[str, threading.Event] = {}
        self.sync = TerminalSync()

    def add_user(self, user_id: str):
        event = threading.Event()
        self.users[user_id] = event
        return event

    def remove_user(self, user_id: str):
        if user_id in self.users:
            del self.users[user_id]

    def broadcast_change(self, change: str):
        self.sync.enqueue_change(change)
        for event in self.users.values():
            event.set()

    def start_session(self):
        self.sync.start_sync()

# Example usage
if __name__ == "__main__":
    session = TerminalSession("session1")
    user_event = session.add_user("user1")
    session.broadcast_change("Change in session")
    session.start_session()