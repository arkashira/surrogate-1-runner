import logging
import os
import json
from datetime import datetime
from pathlib import Path

# Directory where logs will be stored
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

def _get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger instance. The logger writes to a file
    named <name>.log inside the LOG_DIR. Handlers are added only once.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(LOG_DIR / f"{name}.log")
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger

def log_training_event(event: dict) -> None:
    """
    Log a training event. The event dict is JSON‑serialised and written
    to the training log file. The same event is also appended to a
    JSON‑lines file for easy downstream consumption.

    Parameters
    ----------
    event : dict
        Arbitrary key/value pairs describing the training event.
    """
    logger = _get_logger("training")
    logger.info(json.dumps(event))

    # Append to a JSON‑lines file for quick parsing
    jsonl_path = LOG_DIR / "training_events.jsonl"
    with jsonl_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event) + "\n")

def read_training_events() -> list[dict]:
    """
    Return all training events that have been logged so far.
    """
    jsonl_path = LOG_DIR / "training_events.jsonl"
    if not jsonl_path.exists():
        return []

    events = []
    with jsonl_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return events