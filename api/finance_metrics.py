"""
Finance metrics API – daily metrics endpoint.
"""

from datetime import datetime, timedelta
import random
from typing import List

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/finance", tags=["finance"])

# --------------------------------------------------------------------------- #
# Pydantic models
# --------------------------------------------------------------------------- #

class DailyMetric(BaseModel):
    """Single daily metric."""
    date: str          # ISO‑8601 YYYY‑MM‑DD
    net_profit: float
    revenue: float
    expenses: float


class MetricsResponse(BaseModel):
    """Response for /metrics/daily."""
    data: List[DailyMetric]
    range: int
    fetched_at: str   # ISO‑8601 UTC


# --------------------------------------------------------------------------- #
# In‑memory mock store (replace with DB in prod)
# --------------------------------------------------------------------------- #

_FAKE_DATA_STORE: List[DailyMetric] = []

# Populate 60 days of deterministic data
BASE_PROFIT = 1000.0
BASE_REVENUE = 5000.0
BASE_EXPENSES = 4000.0
random.seed(42)  # reproducible

for i in range(60):
    day = datetime.utcnow() - timedelta(days=i)
    profit = round(BASE_PROFIT + i * 5 + random.uniform(-50, 50), 2)
    revenue = round(BASE_REVENUE + i * 10 + random.uniform(-100, 100), 2)
    expenses = round(BASE_EXPENSES + i * 7 + random.uniform(-70, 70), 2)

    _FAKE_DATA_STORE.append(
        DailyMetric(
            date=day.strftime("%Y-%m-%d"),
            net_profit=profit,
            revenue=revenue,
            expenses=expenses,
        )
    )

# Store is newest first
_FAKE_DATA_STORE.sort(key=lambda m: m.date, reverse=True)


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _validate_range(range_days: int) -> int:
    """Clamp and validate the `range` query param."""
    if range_days < 1:
        raise HTTPException(status_code=400, detail="`range` must be >= 1")
    if range_days > 365:
        raise HTTPException(status_code=400, detail="`range` must be <= 365")
    return range_days


def _fetch_metrics(range_days: int) -> List[DailyMetric]:
    """Return the most recent `range_days` metrics."""
    return _FAKE_DATA_STORE[:range_days]


# --------------------------------------------------------------------------- #
# Endpoints
# --------------------------------------------------------------------------- #

@router.get("/metrics/daily", response_model=MetricsResponse)
async def get_daily_metrics(
    range: int = Query(
        default=30,
        ge=1,
        le=365,
        description="Number of days to fetch (1‑365)",
    ),
) -> MetricsResponse:
    """
    Retrieve daily finance metrics for the last `range` days.
    """
    valid_range = _validate_range(range)
    data = _fetch_metrics(valid_range)

    return MetricsResponse(
        data=data,
        range=valid_range,
        fetched_at=datetime.utcnow().isoformat() + "Z",
    )


@router.get("/metrics/daily/{date}", response_model=DailyMetric)
async def get_daily_metric_by_date(date: str) -> DailyMetric:
    """
    Retrieve a single day's metric by ISO‑8601 date (YYYY‑MM‑DD).
    """
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use YYYY-MM-DD",
        )

    # In prod – query the DB
    for metric in _FAKE_DATA_STORE:
        if metric.date == date:
            return metric

    raise HTTPException(status_code=404, detail="Metric not found")