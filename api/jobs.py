"""
Job status API endpoints for the surrogate-1 dashboard.
Provides real-time metrics for ingestion job monitoring.
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel, Field
from enum import Enum

class JobStatus(str, Enum):
    """Job status enumeration."""
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class Job(BaseModel):
    """Job model with status and timestamps."""
    job_id: str = Field(..., description="Unique job identifier")
    status: JobStatus = Field(..., description="Current job status")
    worker_id: Optional[str] = Field(None, description="Worker processing this job")
    shard_id: Optional[int] = Field(None, description="Shard ID assigned to this job")
    started_at: datetime = Field(..., description="Job start timestamp")
    completed_at: Optional[datetime] = Field(None, description="Job completion timestamp")
    error_message: Optional[str] = Field(None, description="Error details if failed")

    @property
    def duration_seconds(self) -> Optional[float]:
        """Calculate job duration in seconds."""
        if self.completed_at and self.started_at:
            return (self.completed_at - self.started_at).total_seconds()
        if self.started_at and self.status == JobStatus.RUNNING:
            return (datetime.utcnow() - self.started_at).total_seconds()

router = APIRouter(prefix="/jobs", tags=["jobs"])

# ----------------------------------------------------------------------
# Pre-populate with some example jobs
_job_store: List[Job] = [
    Job(
        job_id="1",
        status=JobStatus.RUNNING,
        started_at=datetime.utcnow() - timedelta(minutes=5),
    ),
    Job(
        job_id="2",
        status=JobStatus.COMPLETED,
        started_at=datetime.utcnow() - timedelta(hours=1, minutes=30),
        completed_at=datetime.utcnow() - timedelta(hours=1),
    ),
    Job(
        job_id="3",
        status=JobStatus.FAILED,
        started_at=datetime.utcnow() - timedelta(hours=2),
        completed_at=datetime.utcnow() - timedelta(hours=1, minutes=45),
        error_message="Some error occurred",
    ),
    Job(
        job_id="4",
        status=JobStatus.COMPLETED,
        started_at=datetime.utcnow() - timedelta(days=1, hours=3),
        completed_at=datetime.utcnow() - timedelta(days=1, hours=2, minutes=30),
    ),
]

# ----------------------------------------------------------------------
# Pydantic response models
# ----------------------------------------------------------------------
class JobMetrics(BaseModel):
    total_jobs: int
    success_rate: float
    average_duration_seconds: float
    current_workers: int

class JobInfo(BaseModel):
    job_id: str
    status: JobStatus
    worker_id: Optional[str] = None
    shard_id: Optional[int] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    error_message: Optional[str] = None

class JobsResponse(BaseModel):
    metrics: JobMetrics
    jobs: List[JobInfo]

# ----------------------------------------------------------------------
# API endpoint
# ----------------------------------------------------------------------
@router.get("/", response_model=JobsResponse)
def get_jobs(
    start_date: Optional[datetime] = Query(
        None,
        description="Filter jobs that started on or after this date (ISO 8601)",
    ),
    end_date: Optional[datetime] = Query(
        None,
        description="Filter jobs that started on or before this date (ISO 8601)",
    ),
):
    """
    Retrieve job metrics and a list of jobs optionally filtered by a date range.
    """
    jobs = [job for job in _job_store if start_date is None or job.started_at >= start_date]
    if end_date:
        jobs = [job for job in jobs if end_date >= job.started_at]
    metrics = _compute_metrics(jobs)
    job_infos = [
        JobInfo(
            job_id=job.job_id,
            status=job.status,
            worker_id=job.worker_id,
            shard_id=job.shard_id,
            started_at=job.started_at,
            completed_at=job.completed_at,
            duration_seconds=job.duration_seconds,
            error_message=job.error_message,
        )
        for job in jobs
    ]
    return JobsResponse(metrics=metrics, jobs=job_infos)

def _compute_metrics(jobs: List[Job]) -> JobMetrics:
    total = len(jobs)
    if total == 0:
        return JobMetrics(
            total_jobs=0,
            success_rate=0.0,
            average_duration_seconds=0.0,
            current_workers=0,
        )
    successes = sum(1 for j in jobs if j.status == JobStatus.COMPLETED)
    success_rate = successes / total
    durations = [job.duration_seconds for job in jobs if job.duration_seconds]
    avg_duration = sum(durations) / len(durations) if durations else 0.0
    current_workers = sum(1 for j in jobs if j.status == JobStatus.RUNNING)
    return JobMetrics(
        total_jobs=total,
        success_rate=success_rate,
        average_duration_seconds=avg_duration,
        current_workers=current_workers,
    )