"""
Real‑time data streaming for the firewall validation dashboard.

The module exposes an async generator that yields a JSON string of the
latest validation status every 30 seconds.  It pulls data from
`firewall_validator.monitor.get_latest_status()` and serialises it for
the frontend.

Usage (CLI demo):

    python -m dashboard.streamer

In a production app you would hook the generator into a WebSocket
handler or an SSE endpoint.
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from typing import AsyncGenerator

from firewall_validator.monitor import get_latest_status


async def stream_validation_status(
    interval: float = 30.0,
) -> AsyncGenerator[str, None]:
    """
    Async generator that yields a JSON string of the latest validation
    status every `interval` seconds.

    Parameters
    ----------
    interval : float, optional
        Seconds between status pulls. Default is 30.0.

    Yields
    ------
    str
        JSON representation of the status payload.
    """
    while True:
        status = await get_latest_status()
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": status,
        }
        yield json.dumps(payload)
        await asyncio.sleep(interval)


# --------------------------------------------------------------------------- #
# Demo / debugging helper
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    async def _demo() -> None:
        async for msg in stream_validation_status():
            print(msg)

    asyncio.run(_demo())