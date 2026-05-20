import time
from typing import Any


def run_scan(account: str) -> Any:
    """
    Placeholder for the real scanning logic.

    In production this function would invoke the actual scanner
    (e.g. a CLI, a library call, etc.).  For unit‑testing we
    simply sleep for a short period and return a deterministic
    string so that the rest of the system can be exercised.
    """
    time.sleep(0.1)  # Simulate work
    return f"Scan completed for account {account}"