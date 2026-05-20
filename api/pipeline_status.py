from fastapi import APIRouter, Depends
from typing import List
from datetime import datetime
from pydantic import BaseModel
from ..dependencies import get_db_session
from ..models import Pipeline, PipelineStatus

router = APIRouter()

class PipelineStatusResponse(BaseModel):
    id: int
    name: str
    status: str
    last_run_timestamp: datetime

@router.get("/pipelines/status", response_model=List[PipelineStatusResponse])
async def get_pipeline_status(db_session = Depends(get_db_session)):
    pipelines = db_session.query(Pipeline).all()
    pipeline_statuses = []
    for pipeline in pipelines:
        status = db_session.query(PipelineStatus).filter_by(pipeline_id=pipeline.id).order_by(PipelineStatus.timestamp.desc()).first()
        pipeline_statuses.append(PipelineStatusResponse(
            id=pipeline.id,
            name=pipeline.name,
            status=status.status if status else "Unknown",
            last_run_timestamp=status.timestamp if status else None
        ))
    return pipeline_statuses