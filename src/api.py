"""
Core module that implements:

* In‑memory caching of daily total cost
* Deterministic cost calculation (placeholder)
* Background worker that recomputes the previous day’s cost at UTC midnight
"""

import datetime
import threading
import time
from typing import Dict

# --------------------------------------------------------------------------- #
# Cache infrastructure
# --------------------------------------------------------------------------- #
_daily_cost_cache: Dict[str, float] = {}
_cache_lock = threading.Lock()


def _compute_daily_cost_for_date(target_date: datetime.date) -> float:
    """
    Deterministic placeholder for the real cost calculation.
    The function is pure and side‑effect free, making it trivial to
    monkey‑patch in tests.
    """
    epoch = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    ts = int(target_date.replace(tzinfo=datetime.timezone.utc).timestamp())
    return float(ts) / 1_000_000.0


def _cache_daily_cost(target_date: datetime.date) -> None:
    """
    Compute the cost for *target_date* and store it in the cache.
    Thread‑safe.
    """
    cost = _compute_daily_cost_for_date(target_date)
    date_str = target_date.isoformat()
    with _cache_lock:
        _daily_cost_cache[date_str] = cost


def get_daily_cost(date_str: str) -> float:
    """
    Public API to retrieve the cost for a given date.

    Parameters
    ----------
    date_str : str
        ISO‑8601 date string (`YYYY-MM-DD`).

    Returns
    -------
    float
        Total cost for the requested day.
    """
    try:
        target_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"Invalid date format: {date_str}") from exc

    with _cache_lock:
        if date_str in _daily_cost_cache:
            return _daily_cost_cache[date_str]

    # Cache miss – compute and store
    _cache_daily_cost(target_date)
    return _daily_cost_cache[date_str]


# --------------------------------------------------------------------------- #
# Background worker
# --------------------------------------------------------------------------- #
def _next_midnight_utc() -> float:
    """
    Timestamp of the next UTC midnight.
    """
    now = datetime.datetime.utcnow()
    tomorrow = now + datetime.timedelta(days=1)
    midnight = datetime.datetime(
        year=tomorrow.year,
        month=tomorrow.month,
        day=tomorrow.day,
        tzinfo=datetime.timezone.utc,
    )
    return midnight.timestamp()


def _daily_aggregation_worker() -> None:
    """
    Recompute the previous day’s cost at every UTC midnight.
    """
    while True:
        sleep_seconds = _next_midnight_utc() - time.time()
        if sleep_seconds > 0:
            time.sleep(sleep_seconds)

        yesterday = datetime.datetime.utcnow().date() - datetime.timedelta(days=1)
        _cache_daily_cost(yesterday)


def start_daily_aggregation_scheduler() -> None:
    """
    Start the background worker thread.  The function is idempotent;
    subsequent calls are no‑ops.
    """
    if not hasattr(start_daily_aggregation_scheduler, "_thread_started"):
        thread = threading.Thread(
            target=_daily_aggregation_worker,
            name="DailyAggregationWorker",
            daemon=True,
        )
        thread.start()
        start_daily_aggregation_scheduler._thread_started = True