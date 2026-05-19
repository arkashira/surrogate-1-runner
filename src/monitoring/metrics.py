"""
Prometheus metrics endpoint for the surrogate-1 service.

This module exposes a FastAPI router that serves the `/metrics` endpoint
used by Prometheus for scraping.  The metrics registry is shared with the
rest of the application, so any counters, gauges, or histograms defined
elsewhere will automatically appear here.

The endpoint is intentionally lightweight and does not require authentication,
mirroring the behaviour of typical Prometheus scrape targets.
"""

from fastapi import APIRouter, Response
from prometheus_client import generate_latest, REGISTRY, CONTENT_TYPE_LATEST
from starlette.responses import Response as StarletteResponse

# Create a router that can be included in the main FastAPI application.
router = APIRouter()

@router.get("/metrics")
async def metrics() -> StarletteResponse:
    """
    Return the current Prometheus metrics.

    The response is generated from the global `REGISTRY` which contains
    all metrics registered by the application.  The content type is set
    to `text/plain; version=0.0.4; charset=utf-8` as required by Prometheus.
    """
    # `generate_latest` returns bytes; FastAPI will handle the encoding.
    data = generate_latest(REGISTRY)
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)