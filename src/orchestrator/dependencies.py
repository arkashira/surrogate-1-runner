from __future__ import annotations

from threading import Lock
from typing import Dict, Optional

from .models import Agent, Task


class AgentStore:
    """
    Very small in‑memory repository.  In production you would replace this
    with a real DB layer (SQLAlchemy, Prisma, etc.).
    """
    def __init__(self) -> None:
        self._agents: Dict[str, Agent] = {}
        self._lock = Lock()

    # ---------- CRUD ---------- #
    def add(self, agent: Agent) -> None:
        with self._lock:
            self._agents[agent.id] = agent

    def get(self, agent_id: str) -> Optional[Agent]:
        return self._agents.get(agent_id)

    def all(self) -> Dict[str, Agent]:
        return self._agents

    # ---------- Hierarchy helpers ---------- #
    def get_children(self, parent_id: str) -> list[Agent]:
        return [a for a in self._agents.values() if a.parent_id == parent_id]

    def attach_child(self, parent: Agent, child: Agent) -> None:
        """
        Mutates both parent and child to keep the bidirectional link consistent.
        """
        with self._lock:
            parent.children.append(child.id)
            child.parent_id = parent.id
            child.depth = parent.depth + 1
            self._agents[parent.id] = parent
            self._agents[child.id] = child


class TaskQueue:
    """
    Very small in‑memory queue.  Only the API needs to add / read / complete tasks.
    """
    def __init__(self) -> None:
        self._tasks: Dict[str, Task] = {}
        self._lock = Lock()

    def add(self, task: Task) -> None:
        with self._lock:
            self._tasks[task.id] = task

    def get(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)

    def complete(self, task_id: str) -> None:
        with self._lock:
            if task := self._tasks.get(task_id):
                task.status = "completed"
                self._tasks[task_id] = task

    def all(self) -> Dict[str, Task]:
        return self._tasks


# Global, singleton‑style stores used by the FastAPI Depends system
agent_store = AgentStore()
task_queue = TaskQueue()


def get_agent_store() -> AgentStore:
    return agent_store


def get_task_queue() -> TaskQueue:
    return task_queue