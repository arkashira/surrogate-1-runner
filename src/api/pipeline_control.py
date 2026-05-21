from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class PipelineStatus(BaseModel):
    status: str

@router.put("/api/pipelines/{pipeline_id}/pause")
async def pause_pipeline(pipeline_id: int = Path(..., title="The ID of the pipeline to pause")):
    # TO DO: implement the logic to pause the pipeline
    # For now, just return a success message
    return {"message": "Pipeline paused successfully"}

@router.put("/api/pipelines/{pipeline_id}/cancel")
async def cancel_pipeline(pipeline_id: int = Path(..., title="The ID of the pipeline to cancel")):
    # TO DO: implement the logic to cancel the pipeline
    # For now, just return a success message
    return {"message": "Pipeline cancelled successfully"}