"""
Thread‑safe, singleton logger that writes to a dedicated rollback error file.
Provides helpers for error and info logging so callers never need to touch
`logging` directly.
"""

import logging
import os
from datetime import datetime
from threading import Lock
from typing import Optional

# --------------------------------------------------------------------------- #
#  Singleton logger
# --------------------------------------------------------------------------- #
_logger: Optional[logging.Logger] = None
_logger_lock = Lock()


def _get_logger() -> logging.Logger:
    """Return a singleton logger configured for rollback errors."""
    global _logger
    with _logger_lock:
        if _logger is None:
            log_dir = os.getenv("AXENTX_LOG_DIR", "/var/log/axentx")
            os.makedirs(log_dir, exist_ok=True)
            log_path = os.path.join(log_dir, "rollback_errors.log")

            logger = logging.getLogger("axentx.rollback")
            logger.setLevel(logging.DEBUG)          # capture everything
            handler = logging.FileHandler(log_path)
            handler.setFormatter(
                logging.Formatter(
                    fmt="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            )
            logger.addHandler(handler)
            logger.propagate = False
            _logger = logger
        return _logger


# --------------------------------------------------------------------------- #
#  Public helpers
# --------------------------------------------------------------------------- #
def log_error(message: str, exc: Optional[Exception] = None) -> None:
    """Log an error (level ERROR)."""
    logger = _get_logger()
    if exc:
        logger.error(f"{message} | Exception: {exc}", exc_info=exc)
    else:
        logger.error(message)


def log_info(message: str, exc: Optional[Exception] = None) -> None:
    """Log an informational message (level INFO)."""
    logger = _get_logger()
    if exc:
        logger.info(f"{message} | Exception: {exc}", exc_info=exc)
    else:
        logger.info(message)