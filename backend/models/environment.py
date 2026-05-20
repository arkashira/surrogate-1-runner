from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class EnvironmentSettings(BaseModel):
    region: str
    instance_type: str
    vpc_config: dict
    security_groups: List[str]

class Environment(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    settings: EnvironmentSettings
    user_id: str