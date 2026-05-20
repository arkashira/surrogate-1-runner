"""
Metrics collection module for surrogate-1.

This module exposes Prometheus metrics that are updated by the orchestration
layer.  The metrics are:

* WORKFLOW_IN_PROGRESS_GAUGE – number of workflows currently running.
* WORKFLOW_TOTAL_COUNTER – total number of workflows started.
* WORKFLOW_SUCCESS_COUNTER – number of successful workflows.
* WORKFLOW_FAILURE_COUNTER – number of failed workflows.
* WORKFLOW_DURATION_HISTOGRAM – distribution of workflow run times (seconds).
* WORKFLOW_ERROR_LABELS – histogram of error types (optional).

The module also starts an HTTP server on the configured port so that
Prometheus can scrape the metrics.
"""

from __future__ import annotations

import time
import threading
from typing import Callable, Optional

from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    start_http_server,
)

# --------------------------------------------------------------------------- #
# Metric definitions
# --------------------------------------------------------------------------- #

# Gauge for active workflows
WORKFLOW_IN_PROGRESS_GAUGE = Gauge(
    "surrogate_workflow_in_progress",
    "Number of workflow instances currently running",
)

# Counters for workflow lifecycle
WORKFLOW_TOTAL_COUNTER = Counter(
    "surrogate_workflow_total",
    "Total number of workflow instances started",
)

WORKFLOW_SUCCESS_COUNTER = Counter(
    "surrogate_workflow_success_total",
    "Total number of successful workflow instances",
)

WORKFLOW_FAILURE_COUNTER = Counter(
    "surrogate_workflow_failure_total",
    "Total number of failed workflow instances",
)

# Histogram for workflow duration
WORKFLOW_DURATION_HISTOGRAM = Histogram(
    "surrogate_workflow_duration_seconds",
    "Histogram of workflow execution times",
    buckets=(0.1, 0.5, 1, 2, 5, 10, 30, 60, 120, 300, 600),
)

# Optional: error type histogram
WORKFLOW_ERROR_LABELS = Histogram(
    "surrogate_workflow_error_type",
    "Histogram of error types encountered during workflow execution",
    labelnames=("error_type",),
)

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _record_start() -> None:
    """Internal helper to record workflow start."""
    WORKFLOW_IN_PROGRESS_GAUGE.inc()
    WORKFLOW_TOTAL_COUNTER.inc()


def _record_end(success: bool, duration: float, error_type: Optional[str] = None) -> None:
    """Internal helper to record workflow end."""
    WORKFLOW_IN_PROGRESS_GAUGE.dec()
    if success:
        WORKFLOW_SUCCESS_COUNTER.inc()
    else:
        WORKFLOW_FAILURE_COUNTER.inc()
        if error_type:
            WORKFLOW_ERROR_LABELS.labels(error_type=error_type).inc()
    WORKFLOW_DURATION_HISTOGRAM.observe(duration)


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def record_workflow(func: Callable[..., any]) -> Callable[..., any]:
    """
    Decorator that records metrics for a workflow function.

    The wrapped function should return a tuple (success: bool, error: Optional[Exception]).
    """
    def wrapper(*args, **kwargs):
        _record_start()
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            if isinstance(result, tuple) and len(result) == 2:
                success, error = result
            else:
                # Assume success if no error
                success, error = True, None
        except Exception as exc:  # pragma: no cover
            success, error = False, exc
            result = (False, exc)
        duration = time.time() - start_time
        error_type = type(error).__name__ if error else None
        _record_end(success, duration, error_type)
        return result
    return wrapper


def start_metrics_server(port: int = 8000) -> None:
    """
    Starts the Prometheus metrics HTTP server in a background thread.

    The server runs until the process exits.
    """
    def _run_server():
        start_http_server(port)
    thread = threading.Thread(target=_run_server, daemon=True)
    thread.start()