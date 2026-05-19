from typing import Optional
from pydantic import BaseModel

class ResourceMetadata(BaseModel):
    id: str
    name: str
    workspace_id: Optional[str] = None

    class Config:
        orm_mode = True