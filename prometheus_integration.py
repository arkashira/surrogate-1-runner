"""
Prometheus integration for cost spike monitoring.

This module exposes a simple HTTP endpoint that serves Prometheus metrics.
It provides helper functions to update the current cost metric and to
increment a counter when a cost spike is detected.

The cost spike detection logic is intentionally simple: it compares the
current cost against a user‑defined threshold (default 10% increase).
"""

import os
import threading
import time
from typing import Callable

from prometheus_client import Gauge, Counter, start_http_server, REGISTRY

# Metric definitions
COST_CURRENT_GAUGE = Gauge(
    "surrogate_cost_current",
    "Current cost in USD",
    ["resource"],
)
COST_SPIKE_COUNTER = Counter(
    "surrogate_cost_spike_total",
    "Total number of detected cost spikes",
    ["resource"],
)

# Default spike detection threshold (percentage increase)
DEFAULT_SPIKE_THRESHOLD = float(os.getenv("COST_SPIKE_THRESHOLD", "10.0"))


def _detect_spike(prev: float, curr: float, threshold: float) -> bool:
    """
    Return True if the percentage increase from prev to curr exceeds threshold.
    """
    if prev <= 0:
        return False
    percent_increase = ((curr - prev) / prev) * 100
    return percent_increase >= threshold


class CostMonitor:
    """
    Simple cost monitor that tracks the last reported cost per resource
    and updates Prometheus metrics accordingly.
    """

    def __init__(self, threshold: float = DEFAULT_SPIKE_THRESHOLD):
        self.threshold = threshold
        self._last_cost = {}
        self._lock = threading.Lock()

    def update_cost(self, resource: str, cost: float):
        """
        Update the current cost for a given resource. If a spike is detected
        compared to the previous value, the spike counter is incremented.
        """
        with self._lock:
            prev = self._last_cost.get(resource, 0.0)
            if _detect_spike(prev, cost, self.threshold):
                COST_SPIKE_COUNTER.labels(resource=resource).inc()
            COST_CURRENT_GAUGE.labels(resource=resource).set(cost)
            self._last_cost[resource] = cost

    def get_last_cost(self, resource: str) -> float:
        """Return the last recorded cost for a resource."""
        with self._lock:
            return self._last_cost.get(resource, 0.0)


def start_prometheus_server(port: int = 8000, monitor: CostMonitor | None = None):
    """
    Start a Prometheus metrics HTTP server on the given port.
    If a monitor is provided, it will be used to expose metrics.
    """
    start_http_server(port)
    # The Prometheus client automatically serves /metrics via the HTTP
    # server started above. No further action is required here.
    # The monitor can be used by external code to push updates.
    return monitor


# Example usage (this block is not executed when imported as a module)
if __name__ == "__main__":
    monitor = CostMonitor()
    start_prometheus_server(8000, monitor)

    # Simulate cost updates
    resources = ["compute", "storage", "network"]
    while True:
        for res in resources:
            # Dummy cost generation
            new_cost = round(100 * (1 + 0.05 * (hash(res) % 10)), 2)
            monitor.update_cost(res, new_cost)
        time.sleep(30)