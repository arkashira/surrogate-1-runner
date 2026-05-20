"""
FastAPI router exposing the daily‑cost endpoint.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict

from .api import get_daily_cost, start_daily_aggregation_scheduler

router = APIRouter()


@router.get("/api/costs/daily", response_model=Dict[str, float])
async def daily_cost(
    date: str = Query(..., regex=r"^\d{4}-\d{2}-\d{2}$")
) -> Dict[str, float]:
    """
    Return the total cost for a specific day.

    Parameters
    ----------
    date : str
        Query parameter in ISO format (`YYYY-MM-DD`).

    Returns
    -------
    dict
        JSON payload: {"date": "<date>", "total_cost": <float>}
    """
    try:
        total_cost = get_daily_cost(date)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {"date": date, "total_cost": total_cost}


# Ensure the background aggregation scheduler starts when the module is imported.
# The worker is a daemon thread, so it will not block shutdown.
start_daily_aggregation_scheduler()