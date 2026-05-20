import logging
from datetime import datetime

from src.config import settings

def log_alert(message: str) -> None:
    logging.basicConfig(
        filename=settings.ALERT_LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info(message)