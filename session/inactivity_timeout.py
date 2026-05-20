import time
import threading
from typing import Dict, Callable, Optional
from datetime import datetime, timedelta

class SessionInactivityTimeout:
    """
    Manages inactivity timeouts for active shell sessions.
    Automatically terminates sessions after a specified period of inactivity.
    """
    
    def __init__(self, timeout_seconds: int = 1800):
        """
        Initialize the inactivity timeout manager.
        
        Args:
            timeout_seconds: Number of seconds of inactivity before session termination
        """
        self.timeout_seconds = timeout_seconds
        self.sessions: Dict[str, Dict] = {}
        self.lock = threading.Lock()
        self.monitor_thread: Optional[threading.Thread] = None
        self._stop_monitor = threading.Event()
        
    def register_session(self, session_id: str, callback: Callable[[str], None]):
        """
        Register a new session with its termination callback.
        
        Args:
            session_id: Unique identifier for the session
            callback: Function to call when session times out
        """
        with self.lock:
            self.sessions[session_id] = {
                'last_activity': datetime.now(),
                'callback': callback,
                'active': True
            }
            
    def update_activity(self, session_id: str):
        """
        Update the last activity timestamp for a session.
        
        Args:
            session_id: Identifier for the session
        """
        with self.lock:
            if session_id in self.sessions:
                self.sessions[session_id]['last_activity'] = datetime.now()
                
    def unregister_session(self, session_id: str):
        """
        Remove a session from tracking.
        
        Args:
            session_id: Identifier for the session
        """
        with self.lock:
            if session_id in self.sessions:
                del self.sessions[session_id]
                
    def start_monitoring(self):
        """Start the monitoring thread."""
        if self.monitor_thread is None or not self.monitor_thread.is_alive():
            self._stop_monitor.clear()
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            
    def stop_monitoring(self):
        """Stop the monitoring thread."""
        self._stop_monitor.set()
        if self.monitor_thread:
            self.monitor_thread.join()
            
    def _monitor_loop(self):
        """Background loop that checks for timed-out sessions."""
        while not self._stop_monitor.wait(60):  # Check every minute
            self._check_for_timeouts()
            
    def _check_for_timeouts(self):
        """Check all sessions for inactivity timeouts."""
        current_time = datetime.now()
        expired_sessions = []
        
        with self.lock:
            for session_id, session_data in self.sessions.items():
                if not session_data['active']:
                    continue
                    
                idle_duration = current_time - session_data['last_activity']
                if idle_duration > timedelta(seconds=self.timeout_seconds):
                    expired_sessions.append(session_id)
                    
        # Execute callbacks outside of lock to avoid deadlocks
        for session_id in expired_sessions:
            try:
                with self.lock:
                    if session_id in self.sessions:
                        callback = self.sessions[session_id]['callback']
                        self.sessions[session_id]['active'] = False
                        
                callback(session_id)
            except Exception as e:
                print(f"Error terminating session {session_id}: {e}")