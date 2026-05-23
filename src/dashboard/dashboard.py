"""
A lightweight Flask application that provides a real‑time cost dashboard
and an API endpoint for cost data.

Features
--------
* `/dashboard` – Renders an HTML table of current cost data.
* `/api/costs` – Returns JSON with the same data for programmatic access.
* Background thread simulates real‑time updates by refreshing the data
  every 30 seconds. In a real deployment this would pull from a billing
  service or database.

The module exposes a `create_app()` factory so it can be imported by
tests or run directly with `python -m dashboard`.
"""

import json
import random
import threading
import time
from datetime import datetime
from typing import Dict, List

from flask import Flask, jsonify, render_template, request

# --------------------------------------------------------------------------- #
# In‑memory store for cost data
# --------------------------------------------------------------------------- #
# The data structure is a list of dictionaries, each representing a cloud
# resource with its current cost. In a production system this would be
# replaced by a database or an external API call.
_cost_data: List[Dict[str, str | float]] = []

# Lock to protect concurrent access to _cost_data
_data_lock = threading.Lock()


def _generate_mock_costs() -> List[Dict[str, str | float]]:
    """
    Generate a list of mock cost entries. Each entry contains:
    - resource_id: unique identifier
    - name: human readable name
    - cost: current cost in USD
    - last_updated: ISO timestamp of the last update
    """
    resources = [
        ("r1", "Compute Engine VM"),
        ("r2", "Cloud Storage Bucket"),
        ("r3", "BigQuery Dataset"),
        ("r4", "Cloud SQL Instance"),
        ("r5", "Pub/Sub Topic"),
    ]
    now = datetime.utcnow().isoformat() + "Z"
    return [
        {
            "resource_id": rid,
            "name": name,
            "cost": round(random.uniform(0.01, 5.00), 2),
            "last_updated": now,
        }
        for rid, name in resources
    ]


def _update_cost_data() -> None:
    """
    Background worker that refreshes the global _cost_data list every
    UPDATE_INTERVAL seconds. The function runs in a daemon thread.
    """
    UPDATE_INTERVAL = 30  # seconds
    while True:
        new_data = _generate_mock_costs()
        with _data_lock:
            _cost_data[:] = new_data
        time.sleep(UPDATE_INTERVAL)


# Start the background thread at import time
threading.Thread(target=_update_cost_data, daemon=True).start()


# --------------------------------------------------------------------------- #
# Flask application factory
# --------------------------------------------------------------------------- #
def create_app() -> Flask:
    """
    Create and configure a Flask application instance.
    """
    app = Flask(__name__, template_folder="templates")

    @app.route("/dashboard")
    def dashboard():
        """
        Render the dashboard template with the latest cost data.
        Supports optional query parameters:
        - sort: column name to sort by (default: 'cost')
        - order: 'asc' or 'desc' (default: 'desc')
        - filter: substring to filter resource names (case‑insensitive)
        """
        sort = request.args.get("sort", "cost")
        order = request.args.get("order", "desc")
        filter_str = request.args.get("filter", "").lower()

        with _data_lock:
            data = list(_cost_data)

        # Filtering
        if filter_str:
            data = [row for row in data if filter_str in row["name"].lower()]

        # Sorting
        reverse = order == "desc"
        try:
            data.sort(key=lambda x: x.get(sort, ""), reverse=reverse)
        except KeyError:
            # Fallback to cost if invalid sort key
            data.sort(key=lambda x: x["cost"], reverse=reverse)

        return render_template("dashboard.html", rows=data, sort=sort, order=order, filter=filter_str)

    @app.route("/api/costs")
    def api_costs():
        """
        Return the current cost data as JSON. Supports the same query
        parameters as the dashboard for filtering and sorting.
        """
        sort = request.args.get("sort", "cost")
        order = request.args.get("order", "desc")
        filter_str = request.args.get("filter", "").lower()

        with _data_lock:
            data = list(_cost_data)

        if filter_str:
            data = [row for row in data if filter_str in row["name"].lower()]

        reverse = order == "desc"
        try:
            data.sort(key=lambda x: x.get(sort, ""), reverse=reverse)
        except KeyError:
            data.sort(key=lambda x: x["cost"], reverse=reverse)

        return jsonify(data)

    return app


# --------------------------------------------------------------------------- #
# CLI entry point
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    app = create_app()
    # Use a simple development server; in production use a WSGI server.
    app.run(host="0.0.0.0", port=5000, debug=True)