import logging
from datetime import datetime

def write_audit_log(message: str):
    log_file = "/var/log/axentx/audit.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {message}\n"

    with open(log_file, "a") as f:
        f.write(log_entry)