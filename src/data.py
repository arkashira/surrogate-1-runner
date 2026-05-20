"""
In‑memory data layer for real‑time benchmarking.

The module provides:
* A Pydantic model describing a benchmark entry.
* Thread‑safe storage of benchmarks.
* Helper functions for filtering, sorting and retrieving “current” vs
  “upgrade” benchmarks.
* An async queue + generator used by the WebSocket endpoint to push
  newly‑added benchmarks to connected clients in real time.
"""

import asyncio
import time
import uuid
from typing import List, Optional, AsyncGenerator

from pydantic import BaseModel, Field


class Benchmark(BaseModel):
    """A single benchmark measurement."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    component: str                     # e.g. "GPU", "CPU", "RAM"
    game: str                          # e.g. "Cyberpunk 2077"
    fps: float                         # measured frames‑per‑second
    is_current: bool = False           # True → user’s current rig
    timestamp: float = Field(default_factory=time.time)


# --------------------------------------------------------------------------- #
# Internal storage – a simple list protected by an asyncio lock.
# --------------------------------------------------------------------------- #
_benchmarks: List[Benchmark] = []
_lock = asyncio.Lock()

# Queue used to broadcast new benchmarks to WebSocket listeners.
_update_queue: asyncio.Queue[Benchmark] = asyncio.Queue()


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
async def add_benchmark(
    component: str,
    game: str,
    fps: float,
    is_current: bool = False,
) -> Benchmark:
    """
    Create a new Benchmark instance, store it, and push it onto the update
    queue so that any live listeners receive the data immediately.
    """
    bench = Benchmark(
        component=component,
        game=game,
        fps=fps,
        is_current=is_current,
    )
    async with _lock:
        _benchmarks.append(bench)
    await _update_queue.put(bench)
    return bench


async def _snapshot() -> List[Benchmark]:
    """Return a shallow copy of the current benchmark list."""
    async with _lock:
        return list(_benchmarks)


async def get_benchmarks(
    component: Optional[str] = None,
    game: Optional[str] = None,
    sort_by: str = "fps",
    descending: bool = True,
) -> List[Benchmark]:
    """
    Retrieve benchmarks optionally filtered by component and/or game,
    then sorted by the requested field.
    """
    benches = await _snapshot()

    if component:
        benches = [b for b in benches if b.component.lower() == component.lower()]
    if game:
        benches = [b for b in benches if b.game.lower() == game.lower()]

    reverse = descending
    if sort_by == "fps":
        benches.sort(key=lambda b: b.fps, reverse=reverse)
    elif sort_by == "timestamp":
        benches.sort(key=lambda b: b.timestamp, reverse=reverse)
    # Add more sort options later if needed.

    return benches


async def get_current_benchmarks(**kwargs) -> List[Benchmark]:
    """Convenience wrapper that forces `is_current=True`."""
    benches = await get_benchmarks(**kwargs)
    return [b for b in benches if b.is_current]


async def get_upgrade_benchmarks(**kwargs) -> List[Benchmark]:
    """Convenience wrapper that forces `is_current=False`."""
    benches = await get_benchmarks(**kwargs)
    return [b for b in benches if not b.is_current]


async def benchmark_updates() -> AsyncGenerator[Benchmark, None]:
    """
    Async generator that yields newly added benchmarks.
    Consumers (e.g. WebSocket handlers) can `async for bench in
    benchmark_updates(): ...` to receive live data.
    """
    while True:
        bench = await _update_queue.get()
        yield bench