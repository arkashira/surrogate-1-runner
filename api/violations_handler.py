from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List

from api.models import Violation
from api.repositories import ViolationRepository, InMemoryViolationRepository

router = APIRouter()


# Dependency injection – replace the impl in main.py for testing
def get_violation_repo() -> ViolationRepository:
    # In production this would be a DB‑backed instance
    return InMemoryViolationRepository()


@router.get(
    "/api/v1/violations",
    response_model=List[Violation],
    summary="Fetch recent violations",
    description=(
        "Returns a list of violations for the requested `account_id`, "
        "sorted by detection time descending, with pagination support."
    ),
)
async def get_violations(
    account_id: str = Query(..., description="Account identifier to filter violations"),
    limit: int = Query(50, ge=1, le=200, description="Max records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    repo: ViolationRepository = Depends(get_violation_repo),
) -> List[Violation]:
    """
    Retrieve recent violations for a given account.
    """
    violations = await repo.get_by_account(
        account_id,
        limit=limit,
        offset=offset,
    )
    # Returning an empty list when no matches is intentional – callers can
    # distinguish “no data” from an error (e.g., malformed account_id).
    return violations