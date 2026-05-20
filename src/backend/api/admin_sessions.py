from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_
from sqlalchemy.orm import Session as DBSession

from .. import db, models
from pydantic import BaseModel

router = APIRouter(prefix="/admin/sessions", tags=["admin_sessions"])


class SessionOut(BaseModel):
    id: int
    user: str
    node: str
    start: datetime
    duration_seconds: Optional[int]
    status: str

    class Config:
        orm_mode = True


class CommandLogEntry(BaseModel):
    timestamp: datetime
    command: str

    class Config:
        orm_mode = True


def _apply_filters(
    query,
    start_date: Optional[datetime],
    end_date: Optional[datetime],
    user: Optional[str],
    node: Optional[str],
):
    if start_date:
        query = query.filter(models.Session.start_time >= start_date)
    if end_date:
        query = query.filter(models.Session.start_time <= end_date)
    if user:
        query = query.join(models.User).filter(models.User.username == user)
    if node:
        query = query.join(models.Node).filter(models.Node.name == node)
    return query


@router.get("/", response_model=List[SessionOut])
def list_sessions(
    start_date: Optional[datetime] = Query(
        None, description="Filter sessions that started on or after this datetime"
    ),
    end_date: Optional[datetime] = Query(
        None, description="Filter sessions that started on or before this datetime"
    ),
    user: Optional[str] = Query(None, description="Filter by username"),
    node: Optional[str] = Query(None, description="Filter by node name"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db_session: DBSession = Depends(db.get_db),
):
    """
    Return a list of shell sessions with optional filtering.
    """
    query = db_session.query(models.Session).join(models.User).join(models.Node)
    query = _apply_filters(query, start_date, end_date, user, node)
    query = query.order_by(models.Session.start_time.desc()).offset(offset).limit(limit)

    sessions = query.all()
    result = []
    for s in sessions:
        duration = (
            int((s.end_time - s.start_time).total_seconds())
            if s.end_time and s.start_time
            else None
        )
        result.append(
            SessionOut(
                id=s.id,
                user=s.user.username,
                node=s.node.name,
                start=s.start_time,
                duration_seconds=duration,
                status=s.status,
            )
        )
    return result


@router.get("/{session_id}/log", response_model=List[CommandLogEntry])
def get_session_log(
    session_id: int,
    db_session: DBSession = Depends(db.get_db),
):
    """
    Return an immutable, timestamp‑ordered list of commands for a given session.
    """
    session = (
        db_session.query(models.Session)
        .filter(models.Session.id == session_id)
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    logs = (
        db_session.query(models.CommandLog)
        .filter(models.CommandLog.session_id == session_id)
        .order_by(models.CommandLog.timestamp.asc())
        .all()
    )
    return [CommandLogEntry(timestamp=log.timestamp, command=log.command) for log in logs]