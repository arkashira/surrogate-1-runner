
from pydantic import BaseModel

class WorkflowPause(BaseModel):
    workflow_id: int