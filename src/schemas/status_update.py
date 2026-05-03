from pydantic import BaseModel

class StatusUpdate(BaseModel):
    status: str
    actor: str
    previous_status: str