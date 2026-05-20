import os
import logging

logger = logging.getLogger(__name__)

def setup_logging():
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

# Ensure logging is configured
setup_logging()