from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import ResourceMetadata

def get_resources_by_workspace_id(session: Session, workspace_id: str) -> List[ResourceMetadata]:
    return session.execute(select(ResourceMetadata).where(ResourceMetadata.workspace_id == workspace_id)).all()