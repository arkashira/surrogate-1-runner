import logging
from logging.handlers import RotatingFileHandler
from typing import Optional
from ..utils.logging_config import setup_logging, get_logging_config

class FirewallValidatorLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirewallValidatorLogger, cls).__new__(cls)
            cls._instance.init()
        return cls._instance

    def init(self):
        self.logger = logging.getLogger("firewall_validator")
        self.logger.setLevel(logging.INFO)
        setup_logging()
        handler = RotatingFileHandler('/var/log/surrogate-1/firewall_validator.log', maxBytes=1000000, backupCount=5)
        formatter = logging.Formatter(get_logging_config())
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

def get_logger():
    return FirewallValidatorLogger()