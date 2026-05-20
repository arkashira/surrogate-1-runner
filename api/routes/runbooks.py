"""
FastAPI router for runbook CRUD operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db, init_db
from ..models.runbook import Runbook
from ..schemas.runbook import RunbookCreate, RunbookResponse

router = APIRouter(prefix="/api/v1/runbooks", tags=["runbooks"])


@router.on_event("startup")
def startup_event():
    """Initialize database tables on application startup."""
    init_db()


@router.post(
    "",
    response_model=RunbookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new runbook",
    description="Creates a new runbook with title, content, and optional tags."
)
def create_runbook(runbook: RunbookCreate, db: Session = Depends(get_db)):
    """
    Create a new runbook entry.
    
    - **title**: Required, 1-255 characters
    - **content**: Required, minimum 1 character
    - **tags**: Optional list of strings
    """
    # Validate title is not empty/whitespace
    if not runbook.title or not runbook.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title cannot be empty or whitespace"
        )

    # Validate content is not empty/whitespace
    if not runbook.content or not runbook.content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Content cannot be empty or whitespace"
        )

    # Convert tags list to comma-separated string (best from Candidate 1)
    tags_str = None
    if runbook.tags:
        tags_str = ",".join(tag.strip() for tag in runbook.tags if tag.strip())

    # Create new runbook
    db_runbook = Runbook(
        title=runbook.title.strip(),
        content=runbook.content,
        tags=tags_str
    )

    db.add(db_runbook)
    db.commit()
    db.refresh(db_runbook)

    return db_runbook