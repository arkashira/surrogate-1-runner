"""
Dashboard module for surrogate‑1.

* A Flask Blueprint (`dashboard_bp`) that renders a cost‑forecast page.
* Forecast data is read from a CSV file (`/opt/axentx/surrogate-1/forecast.csv`).
  The file is expected to have a header row:  date,cost
* A cron job (or any external process) writes the latest 30‑day forecast to that file.
* The user can request a custom period (1‑30 days) via a query string.
"""

from __future__ import annotations

import csv
import datetime
import logging
from pathlib import Path
from typing import List, Tuple

from flask import Blueprint, abort, render_template, request

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
FORECAST_CSV = Path("/opt/axentx/surrogate-1/forecast.csv")
MAX_PERIOD_DAYS = 30
DEFAULT_PERIOD_DAYS = 7

# ----------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------
logger = logging.getLogger(__name__)
# In production, configure a proper handler (file, syslog, etc.)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# ----------------------------------------------------------------------
# Blueprint
# ----------------------------------------------------------------------
dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    template_folder="templates",
    static_folder="static",
)

# ----------------------------------------------------------------------
# CSV helpers
# ----------------------------------------------------------------------
def _read_forecast() -> List[Tuple[datetime.date, float]]:
    """
    Read the forecast CSV and return a list of (date, cost) tuples.
    Raises FileNotFoundError if the file does not exist.
    """
    if not FORECAST_CSV.exists():
        logger.error("Forecast file not found: %s", FORECAST_CSV)
        raise FileNotFoundError(f"Forecast file not found: {FORECAST_CSV}")

    forecast: List[Tuple[datetime.date, float]] = []

    with FORECAST_CSV.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = datetime.datetime.strptime(row["date"], "%Y-%m-%d").date()
                cost = float(row["cost"])
                forecast.append((date, cost))
            except (KeyError, ValueError) as exc:
                # Skip malformed rows but log for debugging
                logger.warning("Skipping malformed row %s: %s", row, exc)

    return forecast


def _filter_forecast(forecast: List[Tuple[datetime.date, float]], period: int) -> List[Tuple[datetime.date, float]]:
    """
    Return the first `period` entries from the forecast list.
    """
    return forecast[:period]


# ----------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------
@dashboard_bp.route("/", methods=["GET"])
def index() -> str:
    """
    Render the dashboard page.

    Query parameters:
        period (int, optional) – number of days to show (1‑30). Defaults to 7.
    """
    # --- Parse & validate period ---------------------------------------
    period_str = request.args.get("period", str(DEFAULT_PERIOD_DAYS))
    try:
        period = int(period_str)
        if not 1 <= period <= MAX_PERIOD_DAYS:
            raise ValueError
    except ValueError:
        logger.info("Invalid period '%s'; falling back to %d", period_str, DEFAULT_PERIOD_DAYS)
        period = DEFAULT_PERIOD_DAYS

    # --- Load forecast -----------------------------------------------
    try:
        forecast = _read_forecast()
    except FileNotFoundError:
        abort(503, description="Forecast data unavailable. Please try again later.")

    # --- Filter to requested period ------------------------------------
    forecast = _filter_forecast(forecast, period)

    # --- Render --------------------------------------------------------
    return render_template(
        "dashboard.html",
        forecast=forecast,
        period=period,
        max_period=MAX_PERIOD_DAYS,
    )


# ----------------------------------------------------------------------
# Template (for reference – put in /opt/axentx/surrogate-1/templates/dashboard.html)
# ----------------------------------------------------------------------
# The following is a minimal Jinja2 template. In a real project you
# would keep this in a separate file, but it is included here for
# completeness.
#
# -------------------------------------------------------------
# {% extends "base.html" %}
# {% block content %}
# <h1>Cost Forecast</h1>
# <form method="get" action="{{ url_for('dashboard.index') }}">
#   <label for="period">Forecast period (days):</label>
#   <input type="number" id="period" name="period" value="{{ period }}" min="1" max="{{ max_period }}">
#   <button type="submit">Update</button>
# </form>
# <h2>Next {{ period }} days</h2>
# <table>
#   <tr><th>Date</th><th>Cost (USD)</th></tr>
#   {% for date, cost in forecast %}
#   <tr>
#     <td>{{ date.isoformat() }}</td>
#     <td>{{ "%.2f"|format(cost) }}</td>
#   </tr>
#   {% endfor %}
# </table>
# {% endblock %}
# -------------------------------------------------------------