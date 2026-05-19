from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from typing import Optional, Tuple, List


def get_audit_logs(
    db: Session,
    *,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    user_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 20,
) -> Tuple[int, List[models.AuditLog]]:
    query = db.query(models.AuditLog)

    if start_date:
        query = query.filter(models.AuditLog.timestamp >= start_date)
    if end_date:
        query = query.filter(models.AuditLog.timestamp <= end_date)
    if user_id:
        query = query.filter(models.AuditLog.user_id == user_id)

    total = query.count()
    logs = (
        query.order_by(models.AuditLog.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return total, logs


def get_all_audit_logs(
    db: Session,
    *,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    user_id: Optional[int] = None,
) -> List[models.AuditLog]:
    query = db.query(models.AuditLog)

    if start_date:
        query = query.filter(models.AuditLog.timestamp >= start_date)
    if end_date:
        query = query.filter(models.AuditLog.timestamp <= end_date)
    if user_id:
        query = query.filter(models.AuditLog.user_id == user_id)

    return query.order_by(models.AuditLog.timestamp.desc()).all()