"""
Metrics module – isolates all data‑access logic.

In a production system the functions below would talk to
* OS‑level battery APIs,
* a local SQLite / InfluxDB store,
* or remote telemetry services.
For now they return deterministic placeholder data that makes the
recommendation engine testable.
"""

from __future__ import annotations
from datetime import datetime, timedelta
from typing import Dict, Any, List


def get_current_metrics() -> Dict[str, Any]:
    """
    Return a dictionary with the *current* battery state.

    Keys
    ----
    charge_level : int
        Current charge percentage (0‑100).
    usage_rate : float
        Average discharge/charge current in mA.
    temp : float
        Battery temperature in °C.
    """
    # ----> Replace these hard‑coded values with real sensor reads <----
    return {
        "charge_level": 85,          # %
        "usage_rate": 150.0,         # mA
        "temp": 37.5,                # °C
    }


def get_historical_trends() -> Dict[str, Any]:
    """
    Return a dictionary with *historical* battery statistics.

    Keys
    ----
    avg_daily_discharge : float
        Average mA discharged per day over the last week.
    peak_usage_times : List[datetime]
        Timestamps (UTC) when the device hit its highest usage.
    """
    # ----> Replace these hard‑coded values with real historical data <----
    now = datetime.utcnow()
    return {
        "avg_daily_discharge": 120.0,          # mA/day
        "peak_usage_times": [
            now - timedelta(hours=2),
            now - timedelta(hours=5),
            now - timedelta(hours=10),
        ],
    }