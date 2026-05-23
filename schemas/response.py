from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import List, Literal
from pydantic import BaseModel, Field, field_validator


# Type aliases for strict validation
ValidationStatus = Literal["pass", "fail"]
IssueSeverity = Literal["error", "warning"]


class ValidationIssue(BaseModel):
    """Represents a single validation issue found in the CloudFront config."""
    message: str = Field(..., description="Detailed error message")
    path: List[str] = Field(..., description="JSON path to the problematic element")
    severity: IssueSeverity = Field(..., description="Severity level: 'error' or 'warning'")

    @field_validator("path", mode="before")
    @classmethod
    def convert_path_to_list(cls, v):
        if isinstance(v, str):
            return v.split(".")
        return v


class ValidationResult(BaseModel):
    """Represents the complete validation result for a CloudFront config."""
    status: ValidationStatus = Field(..., description="Overall validation status: 'pass' or 'fail'")
    issues: List[ValidationIssue] = Field(default_factory=list, description="List of validation issues")
    timestamp: str = Field(..., description="Timestamp of the validation in ISO 8601 format")
    config_hash: str = Field(..., description="SHA-256 hash of the input config for reference")

    @classmethod
    def create(cls, status: ValidationStatus, issues: List[ValidationIssue], config_dict: dict) -> "ValidationResult":
        """Factory method to create a ValidationResult with auto-generated timestamp and hash."""
        config_bytes = json.dumps(config_dict, sort_keys=True).encode("utf-8")
        return cls(
            status=status,
            issues=issues,
            timestamp=datetime.now(timezone.utc).isoformat(),
            config_hash=sha256(config_bytes).hexdigest()
        )


class ValidationResponse(BaseModel):
    """Represents the API response for a validation request."""
    result: ValidationResult = Field(..., description="The validation result")
    processing_time_ms: int = Field(..., description="Time taken to process the request in milliseconds")