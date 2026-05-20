"""
Submission history model for tracking compliance submissions over time.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class SubmissionStatus(str, Enum):
    """Status of a submission."""
    PASS = "pass"
    FAIL = "fail"
    PENDING = "pending"


class SubmissionDetail(BaseModel):
    """Detailed breakdown of individual submission items."""
    id: str = Field(..., description="Unique identifier for this detail entry")
    field_name: str = Field(..., description="Name of the field or check being validated")
    item_id: Optional[str] = Field(None, description="Reference to the original item")
    value: Optional[str] = Field(None, description="The submitted value")
    passed: bool = Field(..., description="Whether this item passed validation")
    status: SubmissionStatus = Field(..., description="Pass/fail status")
    error_message: Optional[str] = Field(None, description="Error details if failed")
    validated_at: datetime = Field(..., description="Timestamp of validation")


class Submission(BaseModel):
    """Main submission history model."""
    id: str = Field(..., description="Unique submission identifier")
    user_id: str = Field(..., description="User who made the submission")
    created_at: datetime = Field(..., description="Submission timestamp")
    status: SubmissionStatus = Field(..., description="Overall pass/fail summary")
    
    # Aggregate counts (from Candidate 2)
    total_items: int = Field(0, description="Total number of items in submission")
    passed_items: int = Field(0, description="Number of items that passed validation")
    failed_items: int = Field(0, description="Number of items that failed validation")
    
    # Detailed breakdown (from both candidates)
    details: List[SubmissionDetail] = Field(default_factory=list, description="Detailed item breakdown")
    
    # Summary (from Candidate 1)
    summary: Optional[str] = Field(None, description="Overall submission summary")
    
    @property
    def pass_rate(self) -> float:
        """Calculate the pass rate percentage (from Candidate 2)."""
        if self.total_items == 0:
            return 0.0
        return (self.passed_items / self.total_items) * 100
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "sub_abc123",
                "user_id": "user_xyz789",
                "created_at": "2024-05-03T10:30:00Z",
                "status": "pass",
                "total_items": 10,
                "passed_items": 9,
                "failed_items": 1,
                "details": [
                    {
                        "id": "det_001",
                        "field_name": "compliance_check",
                        "value": "validated",
                        "passed": True,
                        "status": "pass",
                        "validated_at": "2024-05-03T10:30:00Z"
                    }
                ],
                "summary": "9 of 10 compliance checks passed"
            }
        }


class SubmissionCreate(BaseModel):
    """Model for creating a new submission (from Candidate 1)."""
    user_id: str = Field(..., description="User making the submission")
    details: List[SubmissionDetail] = Field(default_factory=list, description="Submission details")
    summary: Optional[str] = Field(None, description="Submission summary")


class SubmissionFilter(BaseModel):
    """Filter model for querying submissions by date range (both candidates)."""
    user_id: Optional[str] = Field(None, description="Filter by user")
    status: Optional[SubmissionStatus] = Field(None, description="Filter by status")
    start_date: Optional[datetime] = Field(None, description="Filter submissions from this date")
    end_date: Optional[datetime] = Field(None, description="Filter submissions until this date")
    limit: int = Field(50, ge=1, le=100, description="Maximum number of results")
    offset: int = Field(0, ge=0, description="Number of results to skip")


class SubmissionListResponse(BaseModel):
    """Response model for listing submissions."""
    submissions: List[Submission]
    total: int
    limit: int
    offset: int