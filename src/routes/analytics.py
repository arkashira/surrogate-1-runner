"""
Analytics API for page visit statistics.

Provides:
- GET /analytics/stats   : Returns page view counts and a simple heatmap.
- GET /analytics/export  : Exports the same data as CSV.

Both endpoints are protected by JWT authentication and require a database
session to query the `nav_logs` table.
"""

from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import csv
import io

from sqlalchemy.orm import Session
from sqlalchemy import func, select

# Assume these exist in the project
from ..dependencies import get_db, jwt_decode
from ..models import NavLog  # SQLAlchemy model for nav_logs table

router = APIRouter(prefix="/analytics", tags=["analytics"])
security = HTTPBearer()


def _validate_date_range(
    start: Optional[datetime] = Query(None),
    end: Optional[datetime] = Query(None),
) -> tuple[datetime, datetime]:
    """
    Validate and normalize date range. Defaults to last 7 days.
    """
    now = datetime.utcnow()
    if start is None:
        start = now - timedelta(days=7)
    if end is None:
        end = now
    if start > end:
        raise HTTPException(status_code=400, detail="start must be before end")
    return start, end


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    start: Optional[datetime] = Query(None),
    end: Optional[datetime] = Query(None),
):
    """
    Return page view counts and a simple heatmap for the given date range.
    """
    # Verify JWT
    jwt_decode(credentials.credentials)

    start_dt, end_dt = _validate_date_range(start, end)

    # Query page view counts per page
    page_counts = (
        db.query(
            NavLog.page_url,
            func.count(NavLog.id).label("views"),
        )
        .filter(NavLog.timestamp.between(start_dt, end_dt))
        .group_by(NavLog.page_url)
        .all()
    )

    # Simple heatmap: count per hour of day
    heatmap = (
        db.query(
            func.extract("hour", NavLog.timestamp).label("hour"),
            func.count(NavLog.id).label("views"),
        )
        .filter(NavLog.timestamp.between(start_dt, end_dt))
        .group_by("hour")
        .order_by("hour")
        .all()
    )

    return {
        "page_counts": [{"page_url": p, "views": v} for p, v in page_counts],
        "heatmap": [{"hour": int(h), "views": v} for h, v in heatmap],
        "start": start_dt.isoformat(),
        "end": end_dt.isoformat(),
    }


@router.get("/export")
def export_csv(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    start: Optional[datetime] = Query(None),
    end: Optional[datetime] = Query(None),
):
    """
    Export page view counts as CSV.
    """
    jwt_decode(credentials.credentials)

    start_dt, end_dt = _validate_date_range(start, end)

    page_counts = (
        db.query(
            NavLog.page_url,
            func.count(NavLog.id).label("views"),
        )
        .filter(NavLog.timestamp.between(start_dt, end_dt))
        .group_by(NavLog.page_url)
        .all()
    )

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["page_url", "views"])
    for page, views in page_counts:
        writer.writerow([page, views])

    csv_bytes = output.getvalue().encode("utf-8")
    return Response(
        content=csv_bytes,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=analytics.csv"},
    )