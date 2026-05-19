from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc

from .. import models
from ..database import get_db
from ..schemas.match_schema import MatchOut, InteractionCreate, InteractionOut

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/", response_model=List[MatchOut])
def list_matches(
    provider_id: int = Query(..., description="Provider whose matches are requested"),
    min_score: Optional[float] = Query(None, ge=0, le=100, description="Minimum match score filter"),
    max_score: Optional[float] = Query(None, ge=0, le=100, description="Maximum match score filter"),
    focus: Optional[str] = Query(None, description="Investor stage focus filter (case-insensitive)"),
    db: Session = Depends(get_db),
):
    """
    Retrieve matches for a provider.
    - **provider_id**: Mandatory filter.
    - **min_score/max_score**: Optional range for match quality.
    - **focus**: Optional filter for investor stage (e.g., 'Seed').
    Results are sorted by score descending.
    """
    query = db.query(models.Match).filter(models.Match.provider_id == provider_id)

    if min_score is not None:
        query = query.filter(models.Match.score >= min_score)
    
    if max_score is not None:
        query = query.filter(models.Match.score <= max_score)

    if focus:
        # Case-insensitive partial match on stage focus
        query = query.filter(models.Match.stage_focus.ilike(f"%{focus}%"))

    matches = query.order_by(desc(models.Match.score)).all()
    return matches


@router.post(
    "/{match_id}/signal",
    response_model=InteractionOut,
    status_code=status.HTTP_201_CREATED,
)
def signal_interest(
    match_id: int,
    payload: InteractionCreate,
    db: Session = Depends(get_db),
):
    """
    Record a provider's interest in a specific match.
    Creates a row in the `interactions` table to track engagement.
    """
    # 1. Verify the match exists and belongs to the requesting provider
    match = (
        db.query(models.Match)
        .filter(
            and_(
                models.Match.id == match_id,
                models.Match.provider_id == payload.provider_id
            )
        )
        .first()
    )
    
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found or does not belong to this provider.",
        )

    # 2. Create interaction record
    # Use provided timestamp or default to now
    interaction_timestamp = payload.timestamp if payload.timestamp else datetime.utcnow()
    
    new_interaction = models.Interaction(
        provider_id=payload.provider_id,
        match_id=match_id,
        timestamp=interaction_timestamp,
    )
    
    db.add(new_interaction)
    db.commit()
    db.refresh(new_interaction)

    return new_interaction