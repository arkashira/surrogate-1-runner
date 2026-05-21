import json
import time
from typing import List, Dict, Any, Optional

from fastapi import APIRouter, Request, Response, status, Query
from pydantic import BaseModel, Field, validator

router = APIRouter()


# ---------- Pydantic models ----------
class MetricPoint(BaseModel):
    metric: str = Field(..., description="Metric name, e.g. `my.app.latency`")
    points: List[List[float]] = Field(
        ..., description="[[timestamp, value], …] – timestamp is epoch seconds"
    )
    tags: List[str] = Field(default_factory=list, description="Datadog tags")

    @validator("points")
    def _check_points(cls, v):
        if not all(isinstance(p, list) and len(p) == 2 for p in v):
            raise ValueError("Each point must be a [timestamp, value] list")
        return v


class SubmitMetricsRequest(BaseModel):
    series: List[MetricPoint] = Field(..., description="List of metric series")


# ---------- Helpers ----------
def _simulate_latency() -> None:
    """Tiny delay to make the mock feel realistic without hurting startup time."""
    time.sleep(0.01)


# ---------- Endpoints ----------
@router.post(
    "/api/v1/series",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Mock Datadog metric ingestion endpoint",
    response_model=Dict[str, str],
)
async def submit_metrics(request: Request) -> Response:
    """
    Accept a batch of metric series and pretend to ingest them.
    Returns **202 Accepted** with a tiny JSON payload so callers can
    verify they received a proper response.
    """
    _simulate_latency()
    try:
        payload: Dict[str, Any] = await request.json()
        # Let Pydantic do the heavy lifting
        SubmitMetricsRequest(**payload)
    except Exception as exc:
        return Response(
            content=json.dumps({"error": str(exc)}),
            media_type="application/json",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        content=json.dumps({"status": "queued"}),
        media_type="application/json",
        status_code=status.HTTP_202_ACCEPTED,
    )


@router.get(
    "/api/v1/query",
    summary="Mock Datadog metric query endpoint",
    response_model=Dict[str, Any],
)
async def query_metrics(
    from_ts: int = Query(..., alias="from", description="Start epoch seconds"),
    to: int = Query(..., description="End epoch seconds"),
    query: str = Query(..., description="Datadog‑style query string"),
) -> Response:
    """
    Return a deterministic empty time‑series result.
    The shape matches Datadog’s real API so downstream code can parse it unchanged.
    """
    _simulate_latency()
    result = {
        "status": "ok",
        "res_type": "time_series",
        "series": [],
        "from": from_ts,
        "to": to,
        "query": query,
    }
    return Response(
        content=json.dumps(result),
        media_type="application/json",
        status_code=status.HTTP_200_OK,
    )