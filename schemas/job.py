"""
Pydantic schemas for job serialization and validation.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field

from ..models.job import JobStatus


class JobResponse(BaseModel):
    """
    API response schema for job status queries.

    Mirrors the fields exposed by the Job model.
    """
    job_id: str = Field(..., description="Unique job identifier")
    status: JobStatus = Field(..., description="Current job status")
    created_at: datetime = Field(..., description="Job creation timestamp")
    updated_at: datetime = Field(..., description="Last status update timestamp")
    result: Optional[Any] = Field(None, description="Result payload if completed")
    error: Optional[str] = Field(None, description="Error message if failed")

    class Config:
        orm_mode = True          # allow construction from dataclass instances
        use_enum_values = True   # serialise enums as their values
        json_encoders = {        # ensure datetime → ISO‑8601 string
            datetime: lambda dt: dt.isoformat()
        }