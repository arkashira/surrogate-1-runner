from pydantic import BaseModel
from datetime import datetime

class AlertBase(BaseModel):
    name: str
    description: str

class AlertCreate(AlertBase):
    pass

class Alert(AlertBase):
    id: int
    is_noise: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True