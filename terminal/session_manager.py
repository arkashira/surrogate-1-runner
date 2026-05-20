import uuid
from typing import Dict, List
from .session import TerminalSession

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, TerminalSession] = {}

    def create_session(self, owner: str) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = TerminalSession(session_id, owner)
        return session_id

    def join_session(self, session_id: str, user: str) -> bool:
        if session_id in self.sessions:
            self.sessions[session_id].add_user(user)
            return True
        return False

    def get_session(self, session_id: str) -> TerminalSession:
        return self.sessions.get(session_id)

    def list_sessions(self) -> List[str]:
        return list(self.sessions.keys())