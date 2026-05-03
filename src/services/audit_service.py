from typing import Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from src.models.audit import AuditLog

ALLOWED_STATUSES = {"pending", "processing", "completed", "failed", "cancelled"}


def validate_status(status: str) -> None:
    if status not in ALLOWED_STATUSES:
        raise ValueError(
            f"Invalid status '{status}'. Must be one of: {sorted(ALLOWED_STATUSES)}"
        )


def log_status_change(
    db: Session,
    request_id: str,
    old_status: Optional[str],
    new_status: str,
    changed_by: Optional[str] = None,
) -> AuditLog:
    """
    Persist an audit entry for a request status change.
    Validates new_status (and old_status when provided).
    Returns the created AuditLog instance.
    """
    validate_status(new_status)
    if old_status is not None:
        validate_status(old_status)

    entry = AuditLog(
        request_id=request_id,
        field="status",
        old_value=old_status,
        new_value=new_status,
        changed_by=changed_by,
        created_at=datetime.now(timezone.utc),
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry