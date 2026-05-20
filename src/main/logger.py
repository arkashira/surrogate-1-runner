import logging
import sys
from datetime import datetime
from typing import Optional

class AxentxLogger:
    """Centralized logger for surrogate-1 with timestamps and stack traces."""
    
    def __init__(self, name: str = "surrogate-1", level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Console handler with timestamp
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)
    
    def info(self, message: str, *args, **kwargs):
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        self.logger.error(message, *args, **kwargs)
    
    def debug(self, message: str, *args, **kwargs):
        self.logger.debug(message, *args, **kwargs)
    
    def exception(self, message: str, exc_info: Optional[bool] = None):
        """Log exception with full stack trace."""
        if exc_info is None:
            exc_info = True
        self.logger.exception(message, exc_info=exc_info)
    
    def critical(self, message: str, *args, **kwargs):
        self.logger.critical(message, *args, **kwargs)


# Global logger instance
logger = AxentxLogger("surrogate-1")