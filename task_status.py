"""
Task status management for surrogate-1.

This module defines the `TaskStatus` enum, a lightweight `Task` data model,
and helper functions to transition tasks between states.  The primary
behaviour required by the PRD is the ability to automatically mark a
task as completed once the user indicates that it has been finished.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Optional, List, Iterable


class TaskStatus(enum.Enum):
    """
    Enumeration of possible task states.

    * PENDING – Task is created but not yet assigned.
    * ASSIGNED – Task has been assigned to a user but not yet completed.
    * COMPLETED – Task has been finished and marked as such.
    """
    PENDING = "pending"
    ASSIGNED = "assigned"
    COMPLETED = "completed"

    def __str__(self) -> str:
        return self.value


@dataclass
class Task:
    """
    Lightweight representation of a task.

    Attributes
    ----------
    id : int
        Unique identifier for the task.
    title : str
        Short description of the task.
    status : TaskStatus
        Current status of the task.
    assigned_to : Optional[str]
        Username of the user the task is assigned to.
    """
    id: int
    title: str
    status: TaskStatus = TaskStatus.PENDING
    assigned_to: Optional[str] = None

    def assign(self, user: str) -> None:
        """Assign the task to a user and transition status to ASSIGNED."""
        self.assigned_to = user
        self.status = TaskStatus.ASSIGNED

    def complete(self) -> None:
        """Mark the task as completed."""
        if self.status != TaskStatus.ASSIGNED:
            raise ValueError(
                f"Cannot complete task {self.id} because it is not assigned."
            )
        self.status = TaskStatus.COMPLETED

    def is_completed(self) -> bool:
        """Return True if the task is completed."""
        return self.status == TaskStatus.COMPLETED


def auto_mark_completed(tasks: Iterable[Task]) -> List[Task]:
    """
    Iterate over a collection of tasks and automatically mark any that
    have been flagged as completed by the user.

    The function expects that a task is considered "completed" if it
    has an `assigned_to` value and its status is still ASSIGNED.  In
    real-world usage this could be replaced by a check against a
    completion flag or external event.

    Parameters
    ----------
    tasks : Iterable[Task]
        Collection of tasks to process.

    Returns
    -------
    List[Task]
        List of tasks that were updated to COMPLETED.
    """
    updated: List[Task] = []
    for task in tasks:
        # In this simplified model we assume that any assigned task
        # with a non-empty `assigned_to` field is ready to be marked
        # as completed.  The caller can provide additional logic
        # (e.g., checking a `completed_flag` attribute).
        if task.status == TaskStatus.ASSIGNED and task.assigned_to:
            try:
                task.complete()
                updated.append(task)
            except ValueError:
                # Should not happen in this context; ignore.
                pass
    return updated