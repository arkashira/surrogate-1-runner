"""
Prometheus metrics for the *axentx* surrogate service.

* A dedicated CollectorRegistry isolates our metrics from any third‑party
  collectors that might be loaded elsewhere in the process.
* The port is read from the environment (default 8000) – this makes the
  component container‑friendly.
* Helper functions are tiny, pure and easy to mock in unit‑tests.
"""

from __future__ import annotations

import os
import logging
from prometheus_client import Counter, start_http_server, CollectorRegistry, generate_latest

# ----------------------------------------------------------------------
# Registry & metric definition
# ----------------------------------------------------------------------
_registry = CollectorRegistry()

paste_cascade_failures_total = Counter(
    "paste_cascade_failures_total",
    "Total number of paste‑cascade failures",
    registry=_registry,
)

# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def inc_paste_cascade_failure() -> None:
    """
    Increment the ``paste_cascade_failures_total`` counter.

    The function is deliberately tiny – it only mutates the metric and
    writes a debug log entry.  Because it never returns a value, callers
    can treat it as fire‑and‑forget.
    """
    paste_cascade_failures_total.inc()
    logging.getLogger(__name__).debug(
        "Incremented paste_cascade_failures_total metric"
    )


def start_metrics_server(port: int | None = None) -> None:
    """
    Start a Prometheus HTTP endpoint that serves the metrics from the
    dedicated registry.

    Parameters
    ----------
    port:
        TCP port to bind to.  If ``None`` the value of the environment
        variable ``PROMETHEUS_METRICS_PORT`` is used, falling back to
        ``8000``.

    Raises
    ------
    OSError
        If the socket cannot be bound (e.g. port already in use).
    """
    if port is None:
        port = int(os.getenv("PROMETHEUS_METRICS_PORT", "8000"))

    try:
        start_http_server(port, registry=_registry)
        logging.getLogger(__name__).info(
            "Prometheus metrics server started on port %s", port
        )
    except Exception as exc:  # pragma: no cover – defensive
        logging.getLogger(__name__).exception(
            "Failed to start Prometheus metrics server"
        )
        raise OSError(f"Could not start metrics server on port {port}") from exc


def expose_metrics_as_text() -> bytes:
    """
    Return the current metrics payload in the Prometheus text format.
    Useful for unit‑tests or ad‑hoc debugging.
    """
    return generate_latest(_registry)


def init_metrics(start_server: bool = True, port: int | None = None) -> None:
    """
    Initialise the metrics subsystem.

    * Registers the metric (already done at import time).
    * Optionally starts the HTTP endpoint.

    This helper mirrors the pattern used in many micro‑service
    frameworks – call it once at program start‑up.
    """
    if start_server:
        start_metrics_server(port)