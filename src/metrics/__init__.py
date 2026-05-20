# Re‑export the public names so callers can simply do
#   from src.metrics import INGESTION_FAILURES_TOTAL
# without needing to know the sub‑module layout.

from .ingestion_metrics import (
    INGESTION_FAILURES_TOTAL,
    INGESTION_RETRIES_TOTAL,
    record_failure,
    record_retry,
)

__all__ = [
    "INGESTION_FAILURES_TOTAL",
    "INGESTION_RETRIES_TOTAL",
    "record_failure",
    "record_retry",
]