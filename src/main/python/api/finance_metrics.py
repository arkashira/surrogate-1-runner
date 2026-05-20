"""
Finance metrics API module.

Provides a single endpoint:

    GET /api/v1/finance/metrics/daily

The endpoint returns the latest daily financial metrics for the
authenticated user, including revenue, expense, and net profit.
All numeric values are returned as locale‑aware currency strings.

The module is designed to be imported and registered with the
main FastAPI application.
"""

from __future__ import annotations

import locale
from datetime import datetime
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------
# Locale for currency formatting – change as needed.
LOCALE = "en_US.UTF-8"

try:
    locale.setlocale(locale.LC_ALL, LOCALE)
except locale.Error:
    # Fallback to the user’s default locale if the requested one is missing.
    locale.setlocale(locale.LC_ALL, "")


# ------------------------------------------------------------------
# Authentication & subscription dependency
# ------------------------------------------------------------------
class User(BaseModel):
    """Minimal user representation used by the dependency."""
    user_id: int
    subscription_active: bool


def get_current_user() -> User:
    """
    Dummy authentication dependency.

    In production replace this with JWT, OAuth2, or session logic.
    """
    # For demo purposes we always return an active user.
    return User(user_id=1, subscription_active=True)


# ------------------------------------------------------------------
# Pydantic response model
# ------------------------------------------------------------------
class FinanceMetrics(BaseModel):
    date: datetime = Field(..., description="Timestamp of the metrics")
    revenue: str = Field(..., description="Revenue formatted as currency")
    expense: str = Field(..., description="Expense formatted as currency")
    net_profit: str = Field(..., description="Net profit formatted as currency")


# ------------------------------------------------------------------
# Helper: format a number as currency
# ------------------------------------------------------------------
def format_currency(value: float) -> str:
    """
    Format a float as a currency string using the configured locale.

    Example: 1234567.89 → "$1,234,567.89"
    """
    # locale.currency adds the symbol and grouping
    return locale.currency(value, grouping=True)


# ------------------------------------------------------------------
# Dummy data source
# ------------------------------------------------------------------
def fetch_latest_metrics(user_id: int) -> Dict[str, float]:
    """
    Simulate fetching the latest daily metrics from a database or external service.
    Replace with real data access logic in production.
    """
    # Static demo data – could be randomised or read from a fixture.
    return {
        "revenue": 123456.78,
        "expense": 98765.43,
        "net_profit": 24691.35,
    }


# ------------------------------------------------------------------
# Router
# ------------------------------------------------------------------
router = APIRouter(prefix="/api/v1/finance/metrics")


@router.get(
    "/daily",
    response_model=FinanceMetrics,
    summary="Get latest daily financial metrics",
    description="Returns the most recent daily revenue, expense, and net profit for the authenticated user.",
)
async def get_daily_finance_metrics(
    current_user: User = Depends(get_current_user),
):
    """
    Endpoint to retrieve the latest daily financial metrics.

    Raises:
        HTTPException: 403 if the user’s subscription is inactive.
    """
    if not current_user.subscription_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Active subscription required to access financial metrics.",
        )

    raw = fetch_latest_metrics(current_user.user_id)

    metrics = FinanceMetrics(
        date=datetime.utcnow(),
        revenue=format_currency(raw["revenue"]),
        expense=format_currency(raw["expense"]),
        net_profit=format_currency(raw["net_profit"]),
    )

    # FastAPI will serialise the Pydantic model automatically,
    # but we return a JSONResponse for explicitness.
    return JSONResponse(content=metrics.dict())


# ------------------------------------------------------------------
# Helper for including the router in the main app
# ------------------------------------------------------------------
def include_in_app(app):
    """Attach this router to a FastAPI instance."""
    app.include_router(router)