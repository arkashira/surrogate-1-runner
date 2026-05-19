"""
Investor Interest API

* GET /investor_interest/ – list providers that have signaled interest.
* POST /investor_interest/{provider_id}/status – update a provider’s status.

The module uses an in‑memory store for demo purposes; replace with a DB
layer in production.  Email notifications are simulated with a print
statement – swap with an async task or SMTP client when ready.
"""

from __future__ import annotations

from enum import Enum
from typing import Dict, List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

# --------------------------------------------------------------------------- #
# Data models
# --------------------------------------------------------------------------- #

class ProviderStatus(str, Enum):
    """Possible status values for a provider."""
    IN_REVIEW = "In Review"
    REJECTED = "Rejected"
    DEAL_CLOSED = "Deal Closed"


class Provider(BaseModel):
    """Represents a provider that has signaled interest."""
    id: int
    name: str
    score: float = Field(..., ge=0, le=100)
    executive_summary: str
    status: ProviderStatus = ProviderStatus.IN_REVIEW
    email: EmailStr


class ProviderStatusUpdate(BaseModel):
    """Request body for updating provider status."""
    status: ProviderStatus


class ProviderResponse(BaseModel):
    """Response model for a provider entry."""
    id: int
    name: str
    score: float
    executive_summary: str
    status: ProviderStatus


# --------------------------------------------------------------------------- #
# In‑memory store (demo only)
# --------------------------------------------------------------------------- #

# Pre‑populate with some demo providers
_investor_interest_store: Dict[int, Provider] = {
    1: Provider(
        id=1,
        name="Acme Corp",
        score=87.5,
        executive_summary="Acme Corp is a leading provider of widgets.",
        status=ProviderStatus.IN_REVIEW,
        email="contact@acme.com",
    ),
    2: Provider(
        id=2,
        name="Beta Solutions",
        score=92.0,
        executive_summary="Beta Solutions specializes in SaaS platforms.",
        status=ProviderStatus.IN_REVIEW,
        email="info@beta.com",
    ),
    3: Provider(
        id=3,
        name="Gamma Industries",
        score=78.3,
        executive_summary="Gamma Industries offers industrial automation services.",
        status=ProviderStatus.IN_REVIEW,
        email="sales@gamma.com",
    ),
}

# --------------------------------------------------------------------------- #
# Router
# --------------------------------------------------------------------------- #

router = APIRouter(prefix="/investor_interest", tags=["Investor Interest"])


def _send_email_notification(provider: Provider, new_status: ProviderStatus) -> None:
    """
    Stub for sending an email.  In production, enqueue a background task
    or call an SMTP service.
    """
    print(
        f"[Email] To: {provider.name} <{provider.email}> - "
        f"Your status has been updated to: {new_status}"
    )


@router.get("/", response_model=List[ProviderResponse])
def list_investor_interest() -> List[ProviderResponse]:
    """
    Return a list of providers that have signaled interest.
    """
    return [
        ProviderResponse(
            id=prov.id,
            name=prov.name,
            score=prov.score,
            executive_summary=prov.executive_summary,
            status=prov.status,
        )
        for prov in _investor_interest_store.values()
    ]


@router.post("/{provider_id}/status", status_code=status.HTTP_200_OK)
def update_provider_status(
    provider_id: int, payload: ProviderStatusUpdate
) -> dict:
    """
    Update the status of a provider and persist the change.
    """
    provider = _investor_interest_store.get(provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    provider.status = payload.status
    _send_email_notification(provider, payload.status)

    return {
        "message": "Status updated successfully",
        "new_status": provider.status,
    }