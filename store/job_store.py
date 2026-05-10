"""
Thread-safe Job store implementation with deduplication and strong typing.

This module provides an in-memory job store that:
- Enforces unique job IDs (deduplication).
- Is thread-safe for concurrent API access.
- Uses strong typing (Dataclasses/Enums) for reliability.
- Supports job lifecycle tracking (Queued -> Running -> Completed/Failed).
"""

from __future__ import annotations

import json
import threading
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


class JobPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


class JobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Job:
    job_id: str
    target: str
    config: dict
    priority: JobPriority = JobPriority.NORMAL
    status: JobStatus = JobStatus.QUEUED


class JobStore:
    """
    Thread-safe in-memory job store with deduplication.
    """

    def __init__(self) -> None:
        # Lock to ensure thread safety during read/write operations
        self._lock = threading.RLock()
        self._jobs: Dict[str, Job] = {}

    def add_job(
        self, job_id: str, target: str, config: dict, priority: str = "normal"
    ) -> Job:
        """
        Add a new job to the store.

        Raises:
            ValueError: If a job with the same job_id already exists or priority is invalid.
        """
        with self._lock:
            if job_id in self._jobs:
                raise ValueError(f"Duplicate job_id '{job_id}' detected")

            try:
                priority_enum = JobPriority(priority.lower())
            except ValueError as exc:
                raise ValueError(
                    f"Invalid priority '{priority}'. Allowed: low, normal, high"
                ) from exc

            job = Job(
                job_id=job_id,
                target=target,
                config=config,
                priority=priority_enum,
                status=JobStatus.QUEUED,
            )
            self._jobs[job_id] = job
            return job

    def get_job(self, job_id: str) -> Optional[Job]:
        """Retrieve a job by its ID, or None if not found."""
        with self._lock:
            return self._jobs.get(job_id)

    def update_status(self, job_id: str, status: str) -> bool:
        """
        Update the status of an existing job.

        Returns:
            bool: True if status was updated, False if job not found.
        """
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return False
            
            try:
                job.status = JobStatus(status.lower())
                return True
            except ValueError:
                # Optionally raise or return False for invalid status
                return False

    def list_jobs(self) -> Dict[str, Job]:
        """Return a copy of all jobs."""
        with self._lock:
            return dict(self._jobs)

    def to_json(self) -> str:
        """Serialize the store to JSON for debugging."""
        with self._lock:
            # Convert Enums to strings for JSON serialization
            serializable_jobs = {
                jid: {
                    "job_id": job.job_id,
                    "target": job.target,
                    "config": job.config,
                    "priority": job.priority.value,
                    "status": job.status.value,
                }
                for jid, job in self._jobs.items()
            }
            return json.dumps(serializable_jobs, indent=2)


# Singleton instance for application-wide usage
job_store = JobStore()


# Simple unit tests to verify logic
if __name__ == "__main__":
    store = JobStore()

    # 1. Test adding a job
    job1 = store.add_job("job-123", "dataset1", {"param": 42}, priority="high")
    assert job1.job_id == "job-123"
    assert job1.priority == JobPriority.HIGH
    assert job1.status == JobStatus.QUEUED

    # 2. Test duplicate rejection
    try:
        store.add_job("job-123", "dataset2", {}, priority="low")
    except ValueError as e:
        assert "Duplicate job_id" in str(e)
    else:
        raise AssertionError("Duplicate job_id did not raise ValueError")

    # 3. Test status update
    success = store.update_status("job-123", "running")
    assert success is True
    updated_job = store.get_job("job-123")
    assert updated_job.status == JobStatus.RUNNING

    # 4. Test thread safety (basic simulation)
    import threading
    
    def add_many_jobs(start_idx, count):
        for i in range(start_idx, start_idx + count):
            try:
                store.add_job(f"thread-job-{i}", "target", {})
            except ValueError:
                pass # Ignore duplicates in this specific test

    t1 = threading.Thread(target=add_many_jobs, args=(0, 100))
    t2 = threading.Thread(target=add_many_jobs, args=(50, 100)) # Intentional overlap
    
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print(f"Total jobs in store: {len(store.list_jobs())}")
    print("All tests passed.")