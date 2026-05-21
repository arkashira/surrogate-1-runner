"""
User management system with role-based access control and audit logging.

Features:
- Add, remove, and modify user roles.
- Role-based access checks.
- Audit logs for user actions.
"""

import datetime
from dataclasses import dataclass, field
from enum import Enum, auto
from functools import wraps
from typing import Dict, List, Set, Callable, Any, Optional
import threading

# --------------------------------------------------------------------------- #
# Role definitions
# --------------------------------------------------------------------------- #
class Role(Enum):
    ADMIN = auto()
    USER = auto()
    VIEWER = auto()

# --------------------------------------------------------------------------- #
# User definition
# --------------------------------------------------------------------------- #
@dataclass
class User:
    username: str
    roles: Set[Role] = field(default_factory=set)

# --------------------------------------------------------------------------- #
# Audit logging
# --------------------------------------------------------------------------- #
@dataclass
class AuditEvent:
    timestamp: datetime.datetime
    username: str
    action: str
    details: Optional[str] = None

class AuditLog:
    """Thread-safe audit log."""
    _lock = threading.Lock()
    _events: List[AuditEvent] = []

    @classmethod
    def record(cls, username: str, action: str, details: Optional[str] = None) -> None:
        event = AuditEvent(
            timestamp=datetime.datetime.utcnow(),
            username=username,
            action=action,
            details=details,
        )
        with cls._lock:
            cls._events.append(event)

    @classmethod
    def get_events(cls) -> List[AuditEvent]:
        with cls._lock:
            return list(cls._events)

# --------------------------------------------------------------------------- #
# User manager
# --------------------------------------------------------------------------- #
class UserManager:
    """In-memory user manager with role-based access control."""
    def __init__(self) -> None:
        self._users: Dict[str, User] = {}
        self._lock = threading.Lock()

    def add_user(self, username: str, roles: Set[Role]) -> None:
        with self._lock:
            if username in self._users:
                raise ValueError(f"User '{username}' already exists.")
            self._users[username] = User(username=username, roles=roles)
            AuditLog.record(username, "add_user", f"Roles: {', '.join(r.name for r in roles)}")

    def remove_user(self, username: str) -> None:
        with self._lock:
            if username not in self._users:
                raise KeyError(f"User '{username}' does not exist.")
            del self._users[username]
            AuditLog.record(username, "remove_user")

    def modify_user_roles(self, username: str, roles: Set[Role]) -> None:
        with self._lock:
            if username not in self._users:
                raise KeyError(f"User '{username}' does not exist.")
            self._users[username].roles = roles
            AuditLog.record(username, "modify_user_roles", f"New roles: {', '.join(r.name for r in roles)}")

    def get_user(self, username: str) -> User:
        with self._lock:
            if username not in self._users:
                raise KeyError(f"User '{username}' does not exist.")
            return self._users[username]

    def check_access(self, username: str, required_role: Role) -> bool:
        """Return True if the user has the required role or higher."""
        user = self.get_user(username)
        # Simple hierarchy: ADMIN > USER > VIEWER
        role_hierarchy = {
            Role.ADMIN: 3,
            Role.USER: 2,
            Role.VIEWER: 1,
        }
        user_level = max(role_hierarchy.get(r, 0) for r in user.roles)
        required_level = role_hierarchy.get(required_role, 0)
        return user_level >= required_level

# --------------------------------------------------------------------------- #
# Thread-local current user context
# --------------------------------------------------------------------------- #
_current_user = threading.local()

def set_current_user(username: str) -> None:
    """Set the current user for the thread."""
    _current_user.username = username

def get_current_user() -> Optional[str]:
    """Get the current user for the thread."""
    return getattr(_current_user, "username", None)

# --------------------------------------------------------------------------- #
# Decorator for role-based access
# --------------------------------------------------------------------------- #
def requires_role(required_role: Role) -> Callable:
    """
    Decorator that ensures the current user has the required role.
    Raises PermissionError if access is denied.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            username = get_current_user()
            if username is None:
                raise PermissionError("No user context set.")
            manager: UserManager = kwargs.get("user_manager")
            if manager is None:
                raise ValueError("UserManager instance must be passed as 'user_manager' kwarg.")
            if not manager.check_access(username, required_role):
                raise PermissionError(f"User '{username}' lacks required role: {required_role.name}")
            return func(*args, **kwargs)
        return wrapper
    return decorator