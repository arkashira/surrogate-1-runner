"""
Workflow management module integrated with secure authentication.

Provides task creation, status updates, and real‑time notifications
via registered callbacks. All operations require a valid JWT token.
"""

import threading
import time
from typing import Callable, Dict, List

from .auth import AuthManager, AuthError


class Task:
    """Represents a single workflow task."""

    def __init__(self, task_id: str, description: str) -> None:
        self.task_id = task_id
        self.description = description
        self.status = "pending"
        self.created_at = time.time()
        self.updated_at = self.created_at

    def __repr__(self) -> str:
        return (
            f"Task(id={self.task_id!r}, status={self.status!r}, "
            f"created_at={self.created_at:.0f})"
        )


class WorkflowManager:
    """
    Manages workflow tasks with authentication and real‑time updates.

    Example usage:
        auth = AuthManager()
        wf = WorkflowManager(auth)
        token = auth.generate_token("alice")
        wf.register_listener(lambda t: print(f"Updated: {t}"))
        wf.create_task(token, "task1", "Process dataset")
        wf.update_task_status(token, "task1", "running")
    """

    def __init__(self, auth_manager: AuthManager) -> None:
        self.auth_manager = auth_manager
        self._tasks: Dict[str, Task] = {}
        self._listeners: List[Callable[[Task], None]] = []
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Listener registration
    # ------------------------------------------------------------------
    def register_listener(self, callback: Callable[[Task], None]) -> None:
        """
        Register a callback that receives a Task instance whenever
        a task is created or its status changes.
        """
        self._listeners.append(callback)

    def _notify(self, task: Task) -> None:
        for callback in self._listeners:
            try:
                callback(task)
            except Exception:
                # Swallow listener errors to avoid breaking workflow
                pass

    # ------------------------------------------------------------------
    # Task operations
    # ------------------------------------------------------------------
    def _require_auth(self, token: str) -> None:
        """
        Verify the token; raise AuthError if invalid.
        """
        self.auth_manager.verify_token(token)

    def create_task(self, token: str, task_id: str, description: str) -> Task:
        """
        Create a new task. Requires a valid JWT token.
        """
        self._require_auth(token)
        with self._lock:
            if task_id in self._tasks:
                raise ValueError(f"Task {task_id!r} already exists")
            task = Task(task_id, description)
            self._tasks[task_id] = task
            self._notify(task)
            return task

    def update_task_status(self, token: str, task_id: str, status: str) -> Task:
        """
        Update the status of an existing task. Requires a valid JWT token.
        """
        self._require_auth(token)
        with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                raise KeyError(f"Task {task_id!r} not found")
            task.status = status
            task.updated_at = time.time()
            self._notify(task)
            return task

    def list_tasks(self, token: str) -> List[Task]:
        """
        Return a list of all tasks. Requires a valid JWT token.
        """
        self._require_auth(token)
        with self._lock:
            return list(self._tasks.values())