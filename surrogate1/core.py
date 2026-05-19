"""Core business logic for Surrogate‑1."""
import logging
import os
import sys
from pathlib import Path

from .logger import get_logger

log = get_logger(__name__)

def run_surrogate1(secure: bool = False) -> None:
    """
    Execute the main functionality of Surrogate‑1.

    Parameters
    ----------
    secure : bool
        When True, the function will read the `SURROGATE1_API_KEY` secret
        and perform any secure‑only operations.

    Raises
    ------
    SystemExit
        If the core logic fails, the process exits with status 1.
    """
    try:
        # Example placeholder for real work
        if secure:
            api_key = os.getenv("SURROGATE1_API_KEY")
            if not api_key:
                raise RuntimeError("SURROGATE1_API_KEY secret is missing")
            log.info("Secure mode enabled – API key present")
        else:
            log.info("Normal mode – no secret required")

        # ---- Insert real business logic here ----
        # For demo purposes we just write a log file
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        (log_dir / "surrogate1.log").write_text("Execution successful\n")

        log.info("Surrogate‑1 execution completed successfully")

    except Exception as exc:
        log.exception("Surrogate‑1 execution failed")
        sys.exit(1)