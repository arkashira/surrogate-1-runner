import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "/opt/axentx/surrogate-1/logs"
ACCESS_LOG = os.path.join(LOG_DIR, "access.log")

os.makedirs(LOG_DIR, exist_ok=True)

def configure_access_logger():
    logger = logging.getLogger("access_logger")
    logger.setLevel(logging.INFO)
    
    # Remove existing handlers if reconfigured
    if logger.hasHandlers():
        logger.handlers.clear()
    
    handler = RotatingFileHandler(
        ACCESS_LOG,
        maxBytes=1024*1024*5,  # 5MB
        backupCount=7,
        encoding='utf-8'
    )
    
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] '
        'User: %(user)s | '
        'Session: %(session_id)s | '
        'Action: %(action)s | '
        'IP: %(ip)s | '
        '%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S%z'
    )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

# Create default logger instance
access_logger = configure_access_logger()