"""
Prometheus metrics for the ingestion pipeline.

This module defines two counters:

* :data:`INGESTION_FAILURES_TOTAL` – total number of ingestion failures after
  all retry attempts.
* :data:`INGESTION_RETRIES_TOTAL` – total number of retry attempts for
  ingestion tasks.

Both counters carry the labels ``dataset`` and ``source`` so that the
metrics can be filtered by the dataset being ingested and the source
(e.g. file path, URL, etc.).

Helper functions :func:`record_failure` and :func:`record_retry` are
provided to increment the counters in a single, consistent place.
"""

from prometheus_client import Counter

# --------------------------------------------------------------------------- #
# Counters
# --------------------------------------------------------------------------- #
INGESTION_FAILURES_TOTAL = Counter(
    "ingestion_failures_total",
    "Total number of ingestion failures after all retry attempts",
    ["dataset", "source"],
)

INGESTION_RETRIES_TOTAL = Counter(
    "ingestion_retries_total",
    "Total number of retry attempts for ingestion tasks",
    ["dataset", "source"],
)

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def record_failure(dataset: str, source: str) -> None:
    """
    Increment the ingestion failures counter.

    Parameters
    ----------
    dataset : str
        Identifier of the dataset being ingested.
    source : str
        Identifier of the source (e.g. file path or URL).
    """
    INGESTION_FAILURES_TOTAL.labels(dataset=dataset, source=source).inc()


def record_retry(dataset: str, source: str) -> None:
    """
    Increment the ingestion retries counter.

    Parameters
    ----------
    dataset : str
        Identifier of the dataset being ingested.
    source : str
        Identifier of the source (e.g. file path or URL).
    """
    INGESTION_RETRIES_TOTAL.labels(dataset=dataset, source=source).inc()


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
__all__ = [
    "INGESTION_FAILURES_TOTAL",
    "INGESTION_RETRIES_TOTAL",
    "record_failure",
    "record_retry",
]