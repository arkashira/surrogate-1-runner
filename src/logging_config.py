import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

def setup_logger():
    """
    Configures the logger for the surrogate-1 application.
    Sets up a rotating file handler with structured logging.
    """
    logger = logging.getLogger('surrogate1')
    logger.setLevel(logging.INFO)

    # Create a rotating file handler
    handler = RotatingFileHandler(
        'surrogate1_actions.log',
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )

    # Define a formatter with timestamp and log level
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger