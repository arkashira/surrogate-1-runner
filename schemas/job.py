"""
Pydantic schema definitions for the surrogate‑1 background job API.

The module contains:

* ``Priority`` – an ``Enum`` of allowed priority levels.
* ``JobCreate`` – the request body for creating a job.
* ``JobResponse`` – the response returned after a successful creation.
"""

from __future__ import annotations

import json
from enum import Enum
from typing import Any, Dict

from pydantic import BaseModel, Field, validator


class Priority(str, Enum):
    """Allowed priority levels for a job."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


class JobCreate(BaseModel):
    """
    Payload for creating a new background job.

    Attributes
    ----------
    job_id : str
        Unique identifier for the job. Must be a non‑empty string.
    target : str
        Destination or processing target. Must be a non‑empty string.
    config : Dict[str, Any]
        Arbitrary JSON‑serialisable configuration for the job.
    priority : Priority
        Execution priority; defaults to ``Priority.NORMAL``.
    """

    job_id: str = Field(..., description="Unique identifier for the job.")
    target: str = Field(..., description="Target system or resource for the job.")
    config: Dict[str, Any] = Field(
        ..., description="Arbitrary JSON configuration for the job."
    )
    priority: Priority = Field(
        Priority.NORMAL,
        description="Execution priority; defaults to 'normal'.",
    )

    @validator("job_id", "target")
    def non_empty_strings(cls, v: str, field):
        """Ensure string fields are not empty or whitespace only."""
        if not v or not v.strip():
            raise ValueError(f"{field.name} must be a non‑empty string")
        return v

    @validator("config")
    def config_must_be_json_serialisable(cls, v: Dict[str, Any]):
        """Validate that the config dictionary can be serialised to JSON."""
        try:
            json.dumps(v)
        except (TypeError, OverflowError) as exc:
            raise ValueError(f"config contains non‑JSON‑serialisable value: {exc}") from exc
        return v

    class Config:
        """Pydantic configuration."""

        anystr_strip_whitespace = True
        use_enum_values = True
        schema_extra = {
            "example": {
                "job_id": "job-12345",
                "target": "ingest",
                "config": {"batch_size": 1000, "retry": True},
                "priority": "normal",
            }
        }


class JobResponse(BaseModel):
    """
    Response model for a successfully created job.

    Attributes
    ----------
    job_id : str
        Unique identifier for the job (echoed back from the request).
    status : Literal["queued"]
        Current status of the job. For creation, this is always ``queued``.
    """

    job_id: str
    status: str = Field("queued", const=True, description="Job status – always 'queued' on creation")