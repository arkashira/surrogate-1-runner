import csv
import io
from datetime import datetime
from typing import Generator

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import AuditLog

router = APIRouter(prefix="/audit", tags=["audit"])


def _csv_row_generator(session: Session) -> Generator[str, None, None]:
    """
    Yield CSV rows for all audit logs in a streaming fashion.
    """
    # Header
    header = ["id", "article_id", "timestamp", "author", "action"]
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(header)
    yield buffer.getvalue()
    buffer.seek(0)
    buffer.truncate(0)

    # Rows
    for log in session.query(AuditLog).order_by(AuditLog.timestamp).all():
        writer.writerow(
            [
                log.id,
                log.article_id,
                log.timestamp.isoformat(),
                log.author,
                log.action,
            ]
        )
        yield buffer.getvalue()
        buffer.seek(0)
        buffer.truncate(0)


@router.get("/export", response_class=StreamingResponse)
def export_audit_logs(session: Session = Depends(get_db)):
    """
    Return all audit logs as a CSV file.

    The response is streamed so that the server never holds the entire
    CSV in memory.
    """
    try:
        csv_gen = _csv_row_generator(session)
        response = StreamingResponse(
            csv_gen,
            media_type="text/csv",
            headers={
                "Content-Disposition": (
                    f"attachment; filename=audit_logs_"
                    f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
                )
            },
        )
        return response
    except Exception as exc:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate audit log CSV: {exc}",
        )