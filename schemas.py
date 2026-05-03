from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TimelineEventCreate(BaseModel):
    timestamp: datetime
    description: str
    actor: Optional[str] = None

class RequestUpdate(BaseModel):
    status: Optional[str] = None
    timeline_events: Optional[List[TimelineEventCreate]] = None
    actor: Optional[str] = None