from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Violation(BaseModel):
    """Read‑only representation of a violation."""
    id: str = Field(..., description="Unique identifier of the violation")
    account_id: str = Field(..., description="Account that owns the resource")
    resource_id: str = Field(..., description="Affected resource")
    rule_id: str = Field(..., description="Rule that was violated")
    severity: Severity = Field(..., description="Severity level")
    timestamp: datetime = Field(..., description="When the violation was detected")

    model_config = {"use_enum_values": True}