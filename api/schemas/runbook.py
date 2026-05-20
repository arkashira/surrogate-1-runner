"""
Pydantic schemas for Runbook API.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class RunbookBase(BaseModel):
    """Base schema with common fields."""
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    tags: Optional[List[str]] = None


class RunbookCreate(RunbookBase):
    """Schema for creating a runbook."""
    pass


class RunbookResponse(RunbookBase):
    """Schema for runbook responses."""
    id: str
    tags: Optional[str]  # Stored as comma-separated string
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True