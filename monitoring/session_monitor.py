import time
import logging
from typing import Dict, List
from collections import defaultdict

class SessionMonitor:
    def __init__(self):
        self.active_sessions: Dict[str, float] = {}
        self.session_disconnections: defaultdict = defaultdict(int)
        self.logger = logging.getLogger(__name__)

    def start_session(self, session_id: str) -> None:
        """Record the start time of a new session."""
        self.active_sessions[session_id] = time.time()
        self.logger.info(f"Session {session_id} started.")

    def end_session(self, session_id: str) -> None:
        """Record the end time of a session and log the duration."""
        if session_id in self.active_sessions:
            start_time = self.active_sessions.pop(session_id)
            duration = time.time() - start_time
            self.logger.info(f"Session {session_id} ended. Duration: {duration:.2f} seconds.")
        else:
            self.logger.warning(f"Attempted to end non-existent session {session_id}.")

    def record_disconnection(self, session_id: str) -> None:
        """Record a disconnection event for a session."""
        self.session_disconnections[session_id] += 1
        self.logger.warning(f"Session {session_id} disconnected. Total disconnections: {self.session_disconnections[session_id]}.")

    def get_active_sessions(self) -> List[str]:
        """Return a list of active session IDs."""
        return list(self.active_sessions.keys())

    def get_disconnection_stats(self) -> Dict[str, int]:
        """Return a dictionary of session IDs and their disconnection counts."""
        return dict(self.session_disconnections)