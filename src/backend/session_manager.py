import time
from datetime import timedelta
from threading import Thread
import logging

class SessionManager:
    """
    A robust session management system with idle timeout functionality.
    Automatically terminates inactive sessions while allowing activity tracking.
    """

    def __init__(self, idle_timeout=300):
        """
        Initialize the session manager with configurable idle timeout.

        Args:
            idle_timeout (int): Maximum allowed inactivity time in seconds (default: 300)
        """
        self.sessions = {}
        self.idle_timeout = idle_timeout
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def start_session(self, session_id):
        """
        Start a new session with the given ID.

        Args:
            session_id (str): Unique identifier for the session
        """
        if session_id in self.sessions:
            self.logger.warning(f"Session {session_id} already exists")
            return

        self.sessions[session_id] = {
            'last_activity': time.time(),
            'active': True
        }

        # Start monitoring thread
        Thread(
            target=self._monitor_idle_time,
            args=(session_id,),
            daemon=True
        ).start()
        self.logger.info(f"Started session {session_id}")

    def _monitor_idle_time(self, session_id):
        """
        Internal method to monitor session activity and terminate if idle.

        Args:
            session_id (str): Session ID to monitor
        """
        while True:
            if session_id not in self.sessions or not self.sessions[session_id]['active']:
                break

            current_time = time.time()
            last_activity = self.sessions[session_id]['last_activity']

            if current_time - last_activity > self.idle_timeout:
                self.terminate_session(session_id)
                break

            time.sleep(60)  # Check every minute

    def record_activity(self, session_id):
        """
        Record activity for a session to reset the idle timer.

        Args:
            session_id (str): Session ID to update
        """
        if session_id in self.sessions:
            self.sessions[session_id]['last_activity'] = time.time()
            self.logger.debug(f"Activity recorded for session {session_id}")
        else:
            self.logger.warning(f"Attempted to record activity for non-existent session {session_id}")

    def terminate_session(self, session_id):
        """
        Terminate a session and clean up resources.

        Args:
            session_id (str): Session ID to terminate
        """
        if session_id in self.sessions:
            self.sessions[session_id]['active'] = False
            self.logger.info(f"Terminating session {session_id} due to inactivity")

            # Clean up underlying resources
            self._cleanup_resources(session_id)

            del self.sessions[session_id]

    def _cleanup_resources(self, session_id):
        """
        Internal method to clean up resources associated with a session.

        Args:
            session_id (str): Session ID to clean up
        """
        # Placeholder for actual resource cleanup logic
        # Example: Kubernetes pod deletion, database cleanup, etc.
        self.logger.info(f"Cleaning up resources for session {session_id}")

    def get_active_sessions(self):
        """
        Get a list of currently active session IDs.

        Returns:
            list: Active session IDs
        """
        return [sid for sid, data in self.sessions.items() if data['active']]