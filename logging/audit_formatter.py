import logging
from datetime import datetime

class SecurityAuditFormatter(logging.Formatter):
    def __init__(self):
        super().__init__(
            fmt='%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S.%f'
        )
        self.log_path = '/var/log/surrogate1/security-audit.log'

    def format(self, record):
        # Enforce specific log structure for security events
        if hasattr(record, 'vulnerability_type'):
            record.msg = self._format_security_event(record)
        return super().format(record)

    def _format_security_event(self, record):
        return (
            f"VULNERABILITY_DETECTED "
            f"request_id={record.request_id} "
            f"method={record.request_method} "
            f"path={record.request_path} "
            f"pattern={record.vulnerability_type} "
            f"user_agent={record.user_agent} "
            f"client_ip={record.client_ip}"
        )

# Configure file handler with proper permissions
handler = logging.FileHandler('/var/log/surrogate1/security-audit.log')
handler.setFormatter(SecurityAuditFormatter())
handler.setLevel(logging.WARNING)