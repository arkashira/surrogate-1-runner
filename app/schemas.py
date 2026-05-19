from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class AuditLogBase(BaseModel):
    timestamp: datetime
    user_id: int
    entity: str
    field_changed: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None


class AuditLogResponse(AuditLogBase):
    id: int

    class Config:
        orm_mode = True


class AuditLogListResponse(BaseModel):
    data: List[AuditLogResponse]
    pagination: dict