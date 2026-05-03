# Add near existing create_request
from typing import List, Optional
from sqlalchemy import desc
from src.models import Request
from src.database import get_db  # adapt to your session handling


def list_requests_by_team(
    team_id: str,
    limit: int = 50,
    offset: int = 0,
    db_session = None
) -> List[Request]:
    """
    Return requests for the given team ordered by created_at desc.
    Uses limit/offset for safe pagination.
    """
    should_close = False
    if db_session is None:
        db_session = next(get_db())
        should_close = True

    try:
        return (
            db_session.query(Request)
            .filter(Request.team_id == team_id)
            .order_by(desc(Request.created_at))
            .limit(limit)
            .offset(offset)
            .all()
        )
    finally:
        if should_close and db_session:
            db_session.close()