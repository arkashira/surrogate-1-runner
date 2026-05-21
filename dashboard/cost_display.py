"""
Real‑time cost dashboard integration for CloudOptimize.

This module provides a Flask web service that exposes the current
cloud cost via a `/cost` endpoint.  The cost is refreshed every
minute by a background thread that queries the cloud provider API.
The implementation is intentionally lightweight and uses a mock
provider for demonstration purposes; replace `MockCloudProvider`
with a real SDK client in production.

Author: axentx-dev-bot
"""

import json
import random
import threading
import time
from datetime import datetime
from typing import Dict

from flask import Flask, jsonify

# --------------------------------------------------------------------------- #
# Mock cloud provider API – replace with real SDK client in production
# --------------------------------------------------------------------------- #
class MockCloudProvider:
    """
    Simulates a cloud provider's cost API.  In a real implementation,
    this would call the provider's SDK or REST endpoint.
    """

    @staticmethod
    def get_current_cost() -> Dict[str, float]:
        """
        Return a dictionary of cost components.
        For example: {"compute": 12.34, "storage": 3.21, "network": 1.00}
        """
        # Simulate cost fluctuations
        return {
            "compute": round(random.uniform(10, 20), 2),
            "storage": round(random.uniform(2, 5), 2),
            "network": round(random.uniform(0.5, 2), 2),
            "total": 0.0,  # placeholder, will be calculated
        }


# --------------------------------------------------------------------------- #
# Dashboard state and background updater
# --------------------------------------------------------------------------- #
class CostDashboard:
    """
    Holds the latest cost data and provides thread‑safe access.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._cost_data: Dict[str, float] = {}
        self._last_updated: datetime | None = None

    def update(self, new_data: Dict[str, float]) -> None:
        with self._lock:
            new_data["total"] = round(sum(v for k, v in new_data.items() if k != "total"), 2)
            self._cost_data = new_data
            self._last_updated = datetime.utcnow()

    def get(self) -> Dict[str, float]:
        with self._lock:
            return dict(self._cost_data)

    def last_updated(self) -> datetime | None:
        with self._lock:
            return self._last_updated


class CostUpdater(threading.Thread):
    """
    Background thread that refreshes cost data every minute.
    """

    def __init__(self, dashboard: CostDashboard, interval: int = 60) -> None:
        super().__init__(daemon=True)
        self.dashboard = dashboard
        self.interval = interval
        self._stop_event = threading.Event()

    def run(self) -> None:
        while not self._stop_event.is_set():
            try:
                raw_cost = MockCloudProvider.get_current_cost()
                self.dashboard.update(raw_cost)
            except Exception as exc:
                # In production, log the error appropriately
                print(f"[CostUpdater] Error fetching cost: {exc}")
            # Sleep until the next minute boundary
            next_run = time.time() + self.interval
            sleep_time = max(0, next_run - time.time())
            self._stop_event.wait(sleep_time)

    def stop(self) -> None:
        self._stop_event.set()


# --------------------------------------------------------------------------- #
# Flask application exposing the cost endpoint
# --------------------------------------------------------------------------- #
app = Flask(__name__)
dashboard = CostDashboard()
updater = CostUpdater(dashboard)
updater.start()


@app.route("/cost", methods=["GET"])
def get_cost():
    """
    Return the latest cost data as JSON.
    """
    data = dashboard.get()
    if not data:
        return jsonify({"error": "No cost data available yet"}), 503
    return jsonify(
        {
            "timestamp": dashboard.last_updated().isoformat() if dashboard.last_updated() else None,
            "cost": data,
        }
    )


# --------------------------------------------------------------------------- #
# Application entry point for development
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Run the Flask dev server on port 5000
    app.run(host="0.0.0.0", port=5000)