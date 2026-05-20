from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ComplianceFindingBase(BaseModel):
    resource_id: str
    resource_type: str
    rule_id: str
    rule_name: str
    severity: str
    description: str

class ComplianceFindingCreate(ComplianceFindingBase):
    pass

class ComplianceFindingResponse(ComplianceFindingBase):
    id: int
    detected_at: datetime
    status: str
    resolved_at: Optional[datetime]

    class Config:
        orm_mode = True