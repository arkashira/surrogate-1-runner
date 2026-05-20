import time
from datetime import datetime, timedelta
from typing import Dict, Optional

class SessionManager:
    def __init__(self, timeout_minutes: int = 30):
        self.sessions: Dict[str, Dict] = {}
        self.timeout = timedelta(minutes=timeout_minutes)

    def add_session(self, session_id: str, user: str, node: str) -> None:
        self.sessions[session_id] = {
            'user': user,
            'node': node,
            'start_time': datetime.now(),
            'last_activity': datetime.now(),
            'status': 'active'
        }

    def update_activity(self, session_id: str) -> None:
        if session_id in self.sessions:
            self.sessions[session_id]['last_activity'] = datetime.now()

    def get_active_sessions(self) -> Dict[str, Dict]:
        current_time = datetime.now()
        active_sessions = {}
        for session_id, session_data in self.sessions.items():
            if session_data['status'] == 'active':
                if current_time - session_data['last_activity'] < self.timeout:
                    active_sessions[session_id] = session_data
                else:
                    self.sessions[session_id]['status'] = 'timed_out'
        return active_sessions

    def terminate_session(self, session_id: str) -> bool:
        if session_id in self.sessions:
            self.sessions[session_id]['status'] = 'terminated'
            return True
        return False

    def get_session(self, session_id: str) -> Optional[Dict]:
        return self.sessions.get(session_id)