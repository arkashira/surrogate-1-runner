from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Iterable, Optional
from task import Task


class TaskStore(ABC):
    """Abstract interface for task persistence."""

    @abstractmethod
    def add(self, task: Task) -> Task: ...

    @abstractmethod
    def get(self, task_id: str) -> Optional[Task]: ...

    @abstractmethod
    def list(self, *, user_id: Optional[str] = None) -> Iterable[Task]: ...

    @abstractmethod
    def update(self, task_id: str, **changes) -> Optional[Task]: ...

    @abstractmethod
    def delete(self, task_id: str) -> bool: ...


class InMemoryTaskStore(TaskStore):
    """Simple in‑memory store – replace with DB in prod."""

    def __init__(self) -> None:
        self._store: Dict[str, Task] = {}

    def add(self, task: Task) -> Task:
        self._store[task.id] = task
        return task

    def get(self, task_id: str) -> Optional[Task]:
        return self._store.get(task_id)

    def list(self, *, user_id: Optional[str] = None) -> Iterable[Task]:
        if user_id:
            return (t for t in self._store.values() if t.assignee == user_id)
        return self._store.values()

    def update(self, task_id: str, **changes) -> Optional[Task]:
        task = self._store.get(task_id)
        if task:
            task.update(**changes)
        return task

    def delete(self, task_id: str) -> bool:
        return self._store.pop(task_id, None) is not None