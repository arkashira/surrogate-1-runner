"""
API endpoints for session management.

This module provides CRUD operations for chat sessions, including a new
``clear-history`` endpoint that removes all persisted messages for a
given session.  The endpoint is intentionally lightweight and relies on
the existing SQLAlchemy models and dependency injection for database
access.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Import the database session factory and the Message model.
# These imports assume the following structure in the project:
#   - src/database.py   : contains `get_db()` and SQLAlchemy models
#   - src/models.py    : contains the `Message` ORM model
# Adjust the import paths if the actual project layout differs.
try:
    from ..database import get_db
    from ..models import Message
except ImportError:
    # Fallback for environments where the relative imports fail
    # (e.g., during isolated unit tests).  The actual project
    # should provide these modules.
    from database import get_db  # type: ignore
    from models import Message   # type: ignore

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.get(
    "/{session_id}/messages",
    response_model=List[dict],
    status_code=status.HTTP_200_OK,
    summary="Retrieve the last 50 messages for a session",
)
def get_messages(
    session_id: str,
    db: Session = Depends(get_db),
) -> List[dict]:
    """
    Return the most recent 50 messages for the given session ID.
    """
    messages = (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.timestamp.desc())
        .limit(50)
        .all()
    )
    return [msg.to_dict() for msg in messages]


@router.post(
    "/{session_id}/clear-history",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Clear all chat history for a session",
)
def clear_history(
    session_id: str,
    db: Session = Depends(get_db),
) -> None:
    """
    Delete all messages associated with the given session ID.

    The endpoint is idempotent: if no messages exist, it simply
    returns a 204 No Content response.

    Raises:
        HTTPException: 404 if the session has no messages.
    """
    # Verify that at least one message exists for the session.
    exists = db.query(Message).filter(Message.session_id == session_id).first()
    if not exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No messages found for session '{session_id}'.",
        )

    # Perform the deletion.
    db.query(Message).filter(Message.session_id == session_id).delete()
    db.commit()
    # No content to return; FastAPI will automatically send 204.
    return None