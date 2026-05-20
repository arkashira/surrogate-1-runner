from __future__ import annotations
import logging
from typing import Any

logger = logging.getLogger(__name__)


class ReviewEngine:
    """
    Minimal review engine that can operate in two modes:
    * **single‑issue** – the default, processes one issue at a time.
    * **multi‑issue** – processes all discovered issues (triggered by --all/--full).
    """

    def __init__(self, config: dict[str, Any] | None = None):
        """
        Initialise the engine.
        Args:
            config: Optional configuration dictionary (future‑proofing).
        """
        self.config = config or {}
        logger.debug("ReviewEngine initialised with config: %s", self.config)

    # --------------------------------------------------------------------- #
    # Public API – these are the methods the CLI (and any other caller) uses
    # --------------------------------------------------------------------- #
    def run_multi_issue_mode(self) -> None:
        """Execute the engine in multi‑issue mode."""
        logger.info("Running review engine in multi‑issue mode")
        # ---- INSERT REAL MULTI‑ISSUE LOGIC HERE ----
        print("Running review engine in multi‑issue mode")

    def run_single_issue_mode(self) -> None:
        """Execute the engine in single‑issue mode."""
        logger.info("Running review engine in single‑issue mode")
        # ---- INSERT REAL SINGLE‑ISSUE LOGIC HERE ----
        print("Running review engine in single‑issue mode")


# ------------------------------------------------------------------------- #
# Helper used by the CLI and also by external code that prefers a functional style
# ------------------------------------------------------------------------- #
def run_review(all_flag: bool = False) -> None:
    """
    Convenience wrapper that creates a ReviewEngine and runs the appropriate mode.
    This mirrors the behaviour of the CLI but is callable from Python code.

    Args:
        all_flag: When True, run in multi‑issue mode; otherwise single‑issue.
    """
    engine = ReviewEngine()
    if all_flag:
        engine.run_multi_issue_mode()
    else:
        engine.run_single_issue_mode()