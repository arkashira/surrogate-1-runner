"""
Job status model for surrogate‑1.

Defines the `JobStatus` enum and a simple dataclass representing a job
with its lifecycle timestamps and optional result or error payloads.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class JobStatus(str, Enum):
    """
    Enumerated job states used throughout the surrogate‑1 system.
    """
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Job:
    """
    Represents a job in the surrogate‑1 system.

    Attributes
    ----------
    job_id : str
        Unique identifier for the job.
    status : JobStatus
        Current status of the job.
    created_at : datetime
        Timestamp when the job was created.
    updated_at : datetime
        Timestamp of the most recent status change.
    result : Any, optional
        Result payload if the job completed successfully.
    error : str, optional
        Error message if the job failed.
    """
    job_id: str
    status: JobStatus
    created_at: datetime
    updated_at: datetime
    result: Optional[Any] = field(default=None)
    error: Optional[str] = field(default=None)

    def to_dict(self) -> dict:
        """
        Convert the Job instance into a serialisable dictionary.
        """
        return {
            "job_id": self.job_id,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "result": self.result,
            "error": self.error,
        }