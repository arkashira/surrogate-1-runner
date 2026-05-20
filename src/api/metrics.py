from fastapi import APIRouter, Response
from prometheus_client import Histogram, generate_latest, CONTENT_TYPE_LATEST

# ----------------------------------------------------------------------
# 1️⃣  Global histogram – the single source of truth for all latency data
# ----------------------------------------------------------------------
workflow_latency_histogram = Histogram(
    "surrogate_workflow_latency_seconds",
    "Latency of surrogate workflows in seconds",
    ["workflow_name", "status"],          # required labels
    buckets=[0.01, 0.05, 0.1, 0.5, 1, 5],  # exactly the list the spec asked for
)

router = APIRouter()


@router.get("/metrics")
def get_metrics() -> Response:
    """
    Expose Prometheus metrics in the format expected by Prometheus
    (`text/plain; version=0.0.4`).
    """
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


def record_workflow_latency(workflow_name: str, status: str, latency_seconds: float) -> None:
    """
    Record a latency observation for a given workflow.

    Parameters
    ----------
    workflow_name: str
        Name of the workflow being measured.
    status: str
        Either "success" or "failure".
    latency_seconds: float
        Observed latency in seconds.
    """
    workflow_latency_histogram.labels(
        workflow_name=workflow_name,
        status=status,
    ).observe(latency_seconds)