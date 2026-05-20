
import os
import socket
from typing import Dict, List

class Session:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.users = []
        self.owner = None

    def add_user(self, user: str):
        if user not in self.users:
            self.users.append(user)

    def remove_user(self, user: str):
        if user in self.users:
            self.users.remove(user)

    def set_owner(self, owner: str):
        if owner not in self.users:
            raise ValueError("User is not a member of the session")
        self.owner = owner

    def get_users(self):
        return self.users

    def get_owner(self):
        return self.owner

def get_active_sessions() -> Dict[str, Session]:
    # Implement session storage here (e.g. database, file system)
    pass

def join_session(session_id: str, user: str):
    session = get_active_sessions()[session_id]
    session.add_user(user)

def leave_session(session_id: str, user: str):
    session = get_active_sessions()[session_id]
    session.remove_user(user)

def set_session_owner(session_id: str, owner: str):
    session = get_active_sessions()[session_id]
    session.set_owner(owner)

# /opt/axentx/surrogate-1/terminal/session.py

import socket
from typing import Dict, List, Optional

class TerminalSession:
    def __init__(self, session_id: str, session: Session):
        self.session_id = session_id
        self.session = session
        self.users = set()
        self.current_user = None

    def start(self):
        self.current_user = socket.gethostname()
        self.session.add_user(self.current_user)

    def stop(self):
        if self.current_user:
            self.session.remove_user(self.current_user)
            self.current_user = None

    def get_active_users(self) -> List[str]:
        return list(self.session.get_users())

    def get_owner(self) -> Optional[str]:
        return self.session.get_owner()

    def is_owner(self) -> bool:
        return self.current_user == self.session.get_owner()

    def transfer_ownership(self, new_owner: str):
        if self.is_owner():
            self.session.set_owner(new_owner)

# ## Summary
- Implemented Session class to manage session ownership and permissions
- Implemented TerminalSession class to handle joining, leaving, and transferring ownership of terminal sessions