from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel
from enum import Enum

router = APIRouter(prefix="/api/v1", tags=["jobs"])

# In-memory job store for demo purposes
# Key: job_id, Value: job data dict
JOB_STORE: Dict[str, Dict[str, Any]] = {}

class JobStatus(str, Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"

class JobResponse(BaseModel):
    job_id: str
    status: JobStatus
    created_at: str
    updated_at: str
    result: Optional[Any] = None
    error: Optional[str] = None

@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: str) -> JobResponse:
    """
    Retrieve the current status and details of a job by its ID.

    Parameters
    ----------
    job_id : str
        The unique identifier of the job to retrieve.

    Returns
    -------
    JobResponse
        The job status and associated metadata.

    Raises
    ------
    HTTPException
        If the job_id does not exist in the store.
    """
    job = JOB_STORE.get(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with id '{job_id}' not found",
        )
    return JobResponse(
        job_id=job["job_id"],
        status=JobStatus(job["status"]),
        created_at=job["created_at"].isoformat() if isinstance(job["created_at"], datetime) else job["created_at"],
        updated_at=job["updated_at"].isoformat() if isinstance(job["updated_at"], datetime) else job["updated_at"],
        result=job.get("result"),
        error=job.get("error"),
    )