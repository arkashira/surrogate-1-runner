from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from ...db.session import get_db                # DB session dependency
from ...db.models.user_prefs import UserPrefs    # The model defined above
from ...auth.dependencies import get_current_user  # Auth dependency returning a User ORM object
from ..schemas.preferences import GamingModeResponse, GamingModeUpdate

router = APIRouter(prefix="/preferences", tags=["preferences"])

@router.get("/gaming-mode", response_model=GamingModeResponse)
def get_gaming_mode(
    current_user: "User" = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return the stored ``gaming_mode`` flag for the authenticated user.
    If the user has never saved a preference we return ``False`` (the
    logical default) without creating a row.
    """
    prefs: Optional[UserPrefs] = (
        db.query(UserPrefs)
        .filter(UserPrefs.user_id == current_user.id)
        .first()
    )
    if prefs is None:
        return GamingModeResponse(gaming_mode=False)
    return GamingModeResponse(gaming_mode=prefs.gaming_mode)


@router.put("/gaming-mode", response_model=GamingModeResponse)
def set_gaming_mode(
    payload: GamingModeUpdate,
    current_user: "User" = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Persist the ``gaming_mode`` flag for the authenticated user.
    The row is created on‑first‑write, otherwise it is updated in‑place.
    """
    prefs: Optional[UserPrefs] = (
        db.query(UserPrefs)
        .filter(UserPrefs.user_id == current_user.id)
        .first()
    )
    if prefs is None:
        prefs = UserPrefs(user_id=current_user.id, gaming_mode=payload.gaming_mode)
        db.add(prefs)
    else:
        prefs.gaming_mode = payload.gaming_mode

    db.commit()
    db.refresh(prefs)          # refresh to get any DB‑side defaults/triggers
    return GamingModeResponse(gaming_mode=prefs.gaming_mode)