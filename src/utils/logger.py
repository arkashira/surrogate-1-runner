import logging
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger
import os

class CollectorLogger:
    def __init__(self):
        self.log_path = "/var/log/axentx/surrogate-1/collector.log"
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        
        self.logger = logging.getLogger("collector")
        self.logger.setLevel(logging.INFO)
        
        handler = RotatingFileHandler(
            self.log_path,
            maxBytes=1024*1024*100,  # 100MB
            backupCount=7
        )
        
        formatter = jsonlogger.JsonFormatter(
            fmt='{"timestamp":"%(asctime)s","level":"%(levelname)s","message":"%(message)s","module":"%(module)s"}'
        )
        
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def info(self, message, **kwargs):
        self.logger.info(message, extra=kwargs)
    
    def error(self, message, **kwargs):
        self.logger.error(message, extra=kwargs)

# Singleton instance
collector_logger = CollectorLogger()