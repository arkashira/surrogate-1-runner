from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Status(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    assignee: Optional[str] = None
    channel_id: Optional[str] = None
    message_ts: Optional[str] = None
    user_id: Optional[str] = None
    id: str = field(default_factory=lambda: f"TASK-{uuid.uuid4().hex[:8].upper()}")
    status: Status = field(default=Status.PENDING)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        """Return a JSON‑serialisable representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "assignee": self.assignee,
            "status": self.status.value,
            "channel_id": self.channel_id,
            "message_ts": self.message_ts,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def update(self, **changes) -> None:
        """Update mutable fields and bump `updated_at`."""
        for key, value in changes.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()