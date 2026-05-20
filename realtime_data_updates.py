"""
Real‑time financial data updater.

* Polls an external HTTP endpoint at a configurable interval.
* Normalises the JSON payload into a small in‑memory cache.
* Exposes a coroutine‑safe API to read the latest snapshot.
* Can be started as a background task in an existing asyncio application.
* Includes a tiny CLI for local debugging.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict

import aiohttp

# --------------------------------------------------------------------------- #
# Logging configuration
# --------------------------------------------------------------------------- #
logger = logging.getLogger("realtime_data_updates")
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
)
logger.addHandler(handler)
logger.setLevel(os.getenv("RDU_LOG_LEVEL", "INFO").upper())

# --------------------------------------------------------------------------- #
# Configuration – can be overridden by environment variables
# --------------------------------------------------------------------------- #
DATA_SOURCE_URL: str = os.getenv(
    "RDU_DATA_SOURCE_URL", "https://api.example.com/financials"
)
POLL_INTERVAL: float = float(os.getenv("RDU_POLL_INTERVAL", "30"))  # seconds
CACHE_TTL: float = float(os.getenv("RDU_CACHE_TTL", "60"))  # seconds, optional

# --------------------------------------------------------------------------- #
# In‑memory cache
# --------------------------------------------------------------------------- #
# The cache is a dict of period -> snapshot.  A snapshot contains
# profit, loss and a UTC timestamp.  The entire cache is protected by
# an asyncio.Lock so reads/writes are safe across coroutines.
_cache: Dict[str, Dict[str, Any]] = {}
_cache_lock = asyncio.Lock()


def get_latest_snapshot(period: str) -> Dict[str, Any]:
    """
    Return the most recent snapshot for *period* (daily, weekly, monthly).
    If the cache is empty for that period, an empty dict is returned.
    """
    return _cache.get(period, {})


async def _fetch_data(session: aiohttp.ClientSession) -> Dict[str, Any]:
    """
    Fetch raw JSON from the external API.
    Raises aiohttp.ClientError on network problems.
    """
    async with session.get(DATA_SOURCE_URL) as resp:
        resp.raise_for_status()
        data = await resp.json()
        logger.debug("Fetched raw data: %s", data)
        return data


def _normalize_snapshot(raw: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Convert the raw API payload into the cache format.
    Adds a UTC ISO‑8601 timestamp to each period.
    """
    now = datetime.utcnow().isoformat() + "Z"
    normalized: Dict[str, Dict[str, Any]] = {}
    for period in ("daily", "weekly", "monthly"):
        period_data = raw.get(period)
        if isinstance(period_data, dict):
            normalized[period] = {**period_data, "timestamp": now}
    return normalized


async def _update_loop(stop_event: asyncio.Event) -> None:
    """
    Background task that polls the external API and updates the cache.
    The loop stops when *stop_event* is set.
    """
    async with aiohttp.ClientSession() as session:
        while not stop_event.is_set():
            try:
                raw = await _fetch_data(session)
                new_cache = _normalize_snapshot(raw)
                async with _cache_lock:
                    _cache.update(new_cache)
                logger.info("Cache updated: %s", new_cache)
            except Exception as exc:  # pragma: no cover
                logger.error("Failed to update cache: %s", exc)
            await asyncio.wait(
                [stop_event.wait()], timeout=POLL_INTERVAL
            )


async def start_background_task() -> asyncio.Task:
    """
    Start the polling loop as a background task.
    Returns the asyncio.Task so the caller can cancel it later.
    """
    stop_event = asyncio.Event()
    task = asyncio.create_task(_update_loop(stop_event))

    # Attach a cleanup callback so the event is set when the task is cancelled.
    def _on_cancel(_):
        stop_event.set()

    task.add_done_callback(_on_cancel)
    logger.info("Started realtime data update task.")
    return task


# --------------------------------------------------------------------------- #
# CLI – useful for local debugging
# --------------------------------------------------------------------------- #
async def _cli() -> None:
    """
    Simple CLI that starts the updater and prints the cache every minute.
    """
    task = await start_background_task()
    try:
        while True:
            await asyncio.sleep(60)
            async with _cache_lock:
                snapshot = json.dumps(_cache, indent=2)
            print(f"\n{datetime.utcnow().isoformat()}Z - Current cache snapshot:")
            print(snapshot)
    except KeyboardInterrupt:
        logger.info("Shutting down CLI.")
    finally:
        task.cancel()
        await task


if __name__ == "__main__":  # pragma: no cover
    asyncio.run(_cli())