import logging
import os
from typing import Optional

# Default log level can be overridden by the SURROGATE_LOG_LEVEL env var
DEFAULT_LOG_LEVEL = os.getenv("SURROGATE_LOG_LEVEL", "INFO").upper()

def setup_logging(
    log_level: Optional[str] = None,
    log_file: Optional[str] = None,
    propagate: bool = False,
) -> None:
    """
    Configure the root logger for surrogate-1.

    Parameters
    ----------
    log_level : str, optional
        Logging level as a string (e.g., 'DEBUG', 'INFO'). Defaults to
        the environment variable SURROGATE_LOG_LEVEL or 'INFO'.
    log_file : str, optional
        Path to a log file. If omitted, logs are emitted to stderr.
    propagate : bool, optional
        Whether to propagate logs to ancestor loggers. Defaults to False.
    """
    level = log_level or DEFAULT_LOG_LEVEL
    numeric_level = getattr(logging, level, logging.INFO)

    logger = logging.getLogger()
    logger.setLevel(numeric_level)
    logger.propagate = propagate

    # Remove any existing handlers to avoid duplicate logs
    if logger.handlers:
        for h in logger.handlers:
            logger.removeHandler(h)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if log_file:
        handler = logging.FileHandler(log_file)
    else:
        handler = logging.StreamHandler()

    handler.setFormatter(formatter)
    logger.addHandler(handler)

def get_logging_config():
    return '%(asctime)s - %(name)s - %(levelname)s - %(message)s'