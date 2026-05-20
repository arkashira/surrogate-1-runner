from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

def get_workflow_metrics_for_period(
    start: datetime,
    end: datetime,
) -> List[Dict[str, Any]]:
    """
    Real implementation would query the production DB / analytics store.
    For this repository we return a deterministic stub so the task can be
    exercised in CI without external services.

    Each dict must contain:
        - project_id (int)
        - latency_ms (float)
        - is_error (bool)
    """
    # Stub – replace with actual ORM / SQL query.
    logger.debug("Fetching raw workflow metrics between %s and %s", start, end)
    return [
        {"project_id": 1, "latency_ms": 120.5, "is_error": False},
        {"project_id": 1, "latency_ms": 250.0, "is_error": True},
        {"project_id": 2, "latency_ms": 98.3, "is_error": False},
        {"project_id": 2, "latency_ms": 180.0, "is_error": False},
    ]