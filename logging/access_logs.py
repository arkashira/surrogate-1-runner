import logging
from datetime import datetime

def log_access(user, action, timestamp=None):
    if not timestamp:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f'{timestamp} - {user} - {action}')

# /opt/axentx/surrogate-1/logging/config.yaml
logging:
  version: 1
  handlers:
    file:
      class: logging.FileHandler
      filename: /opt/axentx/surrogate-1/logs/access.log
  root:
    level: INFO
    handlers: [file]

## Summary
- Added `log_access` function to log user actions with timestamp.
- Configured logging to write access logs to a file.
- No changes needed in existing code as per the given task.