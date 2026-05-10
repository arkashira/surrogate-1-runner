from __future__ import annotations

import hashlib
import json
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, validator

# --------------------------------------------------------------------------- #
# 1️⃣  Pydantic models
# --------------------------------------------------------------------------- #

class Priority(str, Enum):
    low = "low"
    normal = "normal"
    high = "high"


class JobPayload(BaseModel):
    target: str = Field(..., description="Target identifier for the job")
    config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Arbitrary JSON configuration for the job",
    )
    priority: Priority = Field(
        default=Priority.normal,
        description="Job priority level",
    )

    @validator("target")
    def target_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("target must not be empty")
        return v

    @validator("config", pre=True)
    def ensure_json(cls, v: Any) -> Dict[str, Any]:
        """
        Accept a stringified JSON payload and turn it into a dict.
        """
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError as exc:
                raise ValueError("config must be valid JSON") from exc
        return v


class JobResponse(BaseModel):
    job_id: str
    status: str = Field(..., description="Current status of the job")


# --------------------------------------------------------------------------- #
# 2️⃣  In‑memory registry
# --------------------------------------------------------------------------- #

# job_id -> JobPayload
_job_store: Dict[str, JobPayload] = {}

# --------------------------------------------------------------------------- #
# 3️⃣  Helper functions
# --------------------------------------------------------------------------- #

def _make_job_id(payload: JobPayload) -> str:
    """
    Deterministic job_id: <target>-<sha256(config)>[:8]
    """
    # Sort items so that key order does not affect the hash
    config_hash = hashlib.sha256(
        str(sorted(payload.config.items())).encode("utf-8")
    ).hexdigest()[:8]
    return f"{payload.target}-{config_hash}"


def register_job(payload: JobPayload) -> str:
    """
    Store a job. Raises HTTPException (409) if the job_id already exists.
    """
    job_id = _make_job_id(payload)
    if job_id in _job_store:
        raise ValueError("Duplicate job_id")
    _job_store[job_id] = payload
    return job_id


def get_job(job_id: str) -> Optional[JobPayload]:
    return _job_store.get(job_id)