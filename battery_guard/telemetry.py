"""
Telemetry helper for BatteryGuard.

The module is intentionally tiny and has no external dependencies.
All public functions are thread‑safe and non‑blocking.
"""

from __future__ import annotations

import json
import os
import platform
import threading
from datetime import datetime
from typing import Callable, Optional

from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# --------------------------------------------------------------------------- #
# Configuration – can be overridden in tests or by the application
# --------------------------------------------------------------------------- #
_TELEMETRY_ENDPOINT: str = "https://axentx-telemetry.example.com/usage"
_OPT_OUT_FILE: str = os.path.expanduser("~/.batteryguard_telemetry_opt_out")

# --------------------------------------------------------------------------- #
# Helpers – internal, not part of the public API
# --------------------------------------------------------------------------- #
def _is_opted_out() -> bool:
    """Return True if the user has opted out of telemetry."""
    return os.path.isfile(_OPT_OUT_FILE)


def _write_opt_out(state: bool) -> None:
    """Create or delete the opt‑out marker file."""
    if state:
        # Create the file atomically – if it already exists nothing happens
        with open(_OPT_OUT_FILE, "w", encoding="utf-8") as f:
            f.write("opted out")
    else:
        try:
            os.remove(_OPT_OUT_FILE)
        except FileNotFoundError:
            pass


def _post_payload(
    endpoint: str,
    payload: dict,
    timeout: float = 5.0,
    opener: Optional[Callable[[Request], object]] = None,
) -> None:
    """
    Send a JSON payload to *endpoint*.

    *opener* is a callable that accepts a `Request` and returns a file‑like
    object.  It defaults to `urllib.request.urlopen`.  This argument exists
    solely to make the function unit‑testable.
    """
    data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    req = Request(endpoint, data=data, method="POST")
    req.add_header("Content-Type", "application/json")

    try:
        with (opener or urlopen)(req, timeout=timeout) as resp:
            resp.read()  # we don't care about the response body
    except (URLError, HTTPError):
        # Silently ignore any network problems – telemetry is best‑effort
        pass


def _send_async(
    command: str,
    endpoint: str = _TELEMETRY_ENDPOINT,
    opener: Optional[Callable[[Request], object]] = None,
) -> None:
    """Internal helper that fires a daemon thread to send telemetry."""
    if _is_opted_out():
        return

    payload = {
        "command": command,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "os_version": platform.platform(),
    }

    thread = threading.Thread(
        target=_post_payload,
        args=(endpoint, payload, 5.0, opener),
        daemon=True,
    )
    thread.start()


# --------------------------------------------------------------------------- #
# Public API – what the rest of the application imports
# --------------------------------------------------------------------------- #
def send(command: str, *, endpoint: Optional[str] = None, opener: Optional[Callable[[Request], object]] = None) -> None:
    """
    Public entry point used by the CLI.

    Parameters
    ----------
    command:
        The name of the command that was executed.
    endpoint:
        Override the telemetry endpoint (useful for tests).
    opener:
        Inject a custom opener (useful for tests).
    """
    _send_async(command, endpoint or _TELEMETRY_ENDPOINT, opener)


def opt_out() -> None:
    """Create the opt‑out marker file."""
    _write_opt_out(True)


def opt_in() -> None:
    """Remove the opt‑out marker file if it exists."""
    _write_opt_out(False)


def is_opted_out() -> bool:
    """Return True if the user has opted out of telemetry."""
    return _is_opted_out()