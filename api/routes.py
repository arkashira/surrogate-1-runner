from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from .models import JobPayload, JobResponse, register_job

router = APIRouter(prefix="/api/v1", tags=["jobs"])

# --------------------------------------------------------------------------- #
# POST /api/v1/jobs
# --------------------------------------------------------------------------- #

@router.post(
    "/jobs",
    status_code=status.HTTP_201_CREATED,
    response_model=JobResponse,
    responses={
        201: {"description": "Job queued successfully"},
        409: {"description": "Duplicate job_id"},
    },
)
async def submit_job(payload: JobPayload) -> JSONResponse:
    """
    Submit a background job. The job_id is deterministic – the same payload
    cannot be queued twice.
    """
    try:
        job_id = register_job(payload)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Duplicate job_id",
        )

    response = JobResponse(job_id=job_id, status="queued")
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response.dict())