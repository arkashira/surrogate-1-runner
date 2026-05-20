"""
API routes for managing token quota limits per team.

This module exposes CRUD operations for quota settings and a simple
in-memory store. In a production environment this would be backed by
a persistent database, but for the purposes of this feature and tests
an in-memory dictionary is sufficient.

The routes are designed to be mounted on a FastAPI application
via `app.include_router(quota_router)`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

from fastapi import APIRouter, HTTPException, Body, status

# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #
@dataclass
class Quota:
    """Represents a token quota for a team."""
    limit: int
    used: int = field(default=0)

    def to_dict(self) -> Dict[str, int]:
        return {"limit": self.limit, "used": self.used}

# --------------------------------------------------------------------------- #
# In-memory store
# --------------------------------------------------------------------------- #
# In a real system this would be replaced by a database or cache.
_quota_store: Dict[str, Quota] = {}

# --------------------------------------------------------------------------- #
# Router
# --------------------------------------------------------------------------- #
quota_router = APIRouter(prefix="/quota", tags=["quota"])

@quota_router.get("/", status_code=status.HTTP_200_OK)
async def list_quotas() -> Dict[str, Dict[str, int]]:
    """
    Return all quota settings for all teams.
    """
    return {team: quota.to_dict() for team, quota in _quota_store.items()}

@quota_router.get("/{team_id}", status_code=status.HTTP_200_OK)
async def get_quota(team_id: str) -> Dict[str, int]:
    """
    Return the quota for a specific team.
    """
    quota = _quota_store.get(team_id)
    if quota is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Quota for team '{team_id}' not found.")
    return quota.to_dict()

@quota_router.post("/{team_id}", status_code=status.HTTP_201_CREATED)
async def create_or_update_quota(
    team_id: str,
    limit: int = Body(..., embed=True, description="Maximum allowed tokens per period")
) -> Dict[str, int]:
    """
    Create or update the quota limit for a team.
    """
    if limit < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Limit must be non-negative.")
    quota = _quota_store.get(team_id)
    if quota:
        quota.limit = limit
    else:
        _quota_store[team_id] = Quota(limit=limit)
    return _quota_store[team_id].to_dict()

@quota_router.patch("/{team_id}/usage", status_code=status.HTTP_200_OK)
async def increment_usage(
    team_id: str,
    increment: int = Body(..., embed=True, description="Number of tokens to add to usage")
) -> Dict[str, int]:
    """
    Increment the used token count for a team. This is typically called
    by the API gateway after a successful request.
    """
    if increment < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Increment must be non-negative.")
    quota = _quota_store.get(team_id)
    if quota is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Quota for team '{team_id}' not found.")
    quota.used += increment
    return quota.to_dict()

@quota_router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quota(team_id: str) -> None:
    """
    Remove a team's quota configuration.
    """
    if team_id in _quota_store:
        del _quota_store[team_id]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Quota for team '{team_id}' not found.")