from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class CompliancePolicy(BaseModel):
    id: str = Field(..., description="Unique identifier for the compliance policy")
    name: str = Field(..., description="Name of the compliance policy")
    description: str = Field(..., description="Description of the compliance policy")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    is_active: bool = Field(default=True, description="Whether the policy is active")
    rules: List[str] = Field(..., description="List of rules associated with the policy")

    class Config:
        orm_mode = True