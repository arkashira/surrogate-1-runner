import logging
import sys
from pathlib import Path

# Create a log directory if it doesn't exist
LOG_DIR = Path("/var/log/axentx")
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Log file
LOG_FILE = LOG_DIR / "policy_violations.log"

# Configure the root logger once
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),  # useful for Docker/K8s
    ],
)

def get_logger(name: str = __name__) -> logging.Logger:
    """Return a logger configured for the application."""
    return logging.getLogger(name)

def log_policy_violation(resource_id: str, missing_tags: dict, status: str) -> None:
    """Log a policy‑violation remediation attempt."""
    logger = get_logger("policy_violation")
    logger.info(
        f"Resource ID: {resource_id} | Missing Tags: {missing_tags} | Status: {status}"
    )

def log_error(error_message: str) -> None:
    """Log an error message."""
    logger = get_logger("error")
    logger.error(error_message)