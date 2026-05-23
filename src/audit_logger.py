import logging
import hashlib
from datetime import datetime
from pathlib import Path

class AuditLogger:
    def __init__(self, log_dir="/opt/axentx/surrogate-1/logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger("audit_logger")
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(self.log_dir / "audit.log")
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def log_request(self, user_ip, service_type):
        timestamp = datetime.now().isoformat()
        ip_hash = hashlib.sha256(user_ip.encode()).hexdigest()
        log_message = f"Timestamp: {timestamp}, IP Hash: {ip_hash}, Service Type: {service_type}"
        self.logger.info(log_message)

    def cleanup_old_logs(self):
        now = datetime.now()
        for log_file in self.log_dir.glob("*.log"):
            if (now - datetime.fromtimestamp(log_file.stat().st_mtime)).days > 90:
                log_file.unlink()