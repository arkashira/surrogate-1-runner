import logging
import os
import json
from datetime import datetime
from typing import Any, Dict

class StructuredLogger:
    """Structured logger for surrogate-1 paste operations with configurable log levels."""
    
    def __init__(self, name: str = "surrogate-1-paste"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # Configure handler with JSON formatting for structured logs
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            json.dumps({
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "level": logging.getLevelName(logging.INFO),
                "message": "{message}",
                "module": "{module}",
                "function": "{funcName}",
                "line": "{lineno}",
                "extra": "{extra}"
            }, default=str),
            "%(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        # Configure log level from environment variable
        self._configure_log_level()
    
    def _configure_log_level(self) -> None:
        """Configure log level from environment variable LOG_LEVEL."""
        env_level = os.getenv("LOG_LEVEL", "INFO").upper()
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        self.logger.setLevel(level_map.get(env_level, logging.INFO))
    
    def log_paste_attempt(
        self,
        method: str,
        target: str,
        success: bool = True,
        error: str = None,
        **kwargs: Any
    ) -> None:
        """Log a paste operation attempt with timestamp, method, and outcome."""
        log_data = {
            "event": "paste_attempt",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "method": method,
            "target": target,
            "success": success,
            "error": error,
            **kwargs
        }
        
        if success:
            self.logger.info(json.dumps(log_data))
        else:
            self.logger.error(json.dumps(log_data))
    
    def log_paste_failure(
        self,
        method: str,
        target: str,
        error: str,
        details: Dict[str, Any] = None,
        **kwargs: Any
    ) -> None:
        """Log a paste operation failure with detailed error information."""
        log_data = {
            "event": "paste_failure",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "method": method,
            "target": target,
            "error": error,
            "details": details or {},
            **kwargs
        }
        self.logger.error(json.dumps(log_data))
    
    def log_paste_success(
        self,
        method: str,
        target: str,
        data_size: int = 0,
        **kwargs: Any
    ) -> None:
        """Log a successful paste operation."""
        log_data = {
            "event": "paste_success",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "method": method,
            "target": target,
            "data_size": data_size,
            **kwargs
        }
        self.logger.info(json.dumps(log_data))
    
    def log_paste_retry(
        self,
        method: str,
        target: str,
        attempt: int,
        max_attempts: int,
        error: str,
        **kwargs: Any
    ) -> None:
        """Log a paste operation retry."""
        log_data = {
            "event": "paste_retry",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "method": method,
            "target": target,
            "attempt": attempt,
            "max_attempts": max_attempts,
            "error": error,
            **kwargs
        }
        self.logger.warning(json.dumps(log_data))


# Global logger instance
logger = StructuredLogger("surrogate-1-paste")