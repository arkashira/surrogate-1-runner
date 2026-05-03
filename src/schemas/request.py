from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional


class RequestCreate(BaseModel):
    type: str = Field(..., min_length=1, description="Request type (e.g., 'incident', 'task')")
    title: str = Field(..., min_length=1, description="Short title for the request")
    owner: str = Field(..., min_length=1, description="Owner identifier (email or username)")
    sla_target: Optional[str] = Field(None, description="ISO-8601 datetime for SLA target")

    @field_validator("sla_target")
    @classmethod
    def validate_sla_target(cls, v):
        if v is None:
            return None
        try:
            dt = datetime.fromisoformat(v.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("sla_target must be a valid ISO-8601 datetime") from exc
        if dt.tzinfo is None:
            raise ValueError("sla_target must include timezone info")
        if dt <= datetime.now(dt.tzinfo):
            raise ValueError("sla_target must be in the future")
        return v


class RequestResponse(BaseModel):
    id: int
    type: str
    title: str
    owner: str
    sla_target: Optional[str]
    status: str
    created_at: str
    public_url: str


class RequestListResponse(BaseModel):
    requests: list[RequestResponse]