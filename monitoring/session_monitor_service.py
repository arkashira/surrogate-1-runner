import logging
from session_monitor import SessionMonitor

class SessionMonitorService:
    def __init__(self):
        self.monitor = SessionMonitor()
        self.logger = logging.getLogger(__name__)

    def handle_session_start(self, session_id: str) -> None:
        """Handle the start of a new session."""
        self.monitor.start_session(session_id)
        self.logger.info(f"Handling start of session {session_id}.")

    def handle_session_end(self, session_id: str) -> None:
        """Handle the end of a session."""
        self.monitor.end_session(session_id)
        self.logger.info(f"Handling end of session {session_id}.")

    def handle_disconnection(self, session_id: str) -> None:
        """Handle a disconnection event for a session."""
        self.monitor.record_disconnection(session_id)
        self.logger.warning(f"Handling disconnection of session {session_id}.")

    def get_active_sessions(self) -> list:
        """Get the list of active sessions."""
        return self.monitor.get_active_sessions()

    def get_disconnection_stats(self) -> dict:
        """Get the disconnection statistics."""
        return self.monitor.get_disconnection_stats()