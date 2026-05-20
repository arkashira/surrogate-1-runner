import logging
import os
from datetime import datetime

def setup_logging():
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

def log_audit(message, level='INFO'):
    logger = logging.getLogger(__name__)
    logger.log(level, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

# /opt/axentx/surrogate-1/src/core/audit.py
from src.services.logging import log_audit

def log_freedom_link_traffic(service, request):
    log_audit(f"AI service '{service}' routed through Freedom Link: {request}", level='INFO')

# /opt/axentx/surrogate-1/src/services/ai.py
from src.core.audit import log_freedom_link_traffic

def route_through_freedom_link(service, request):
    # Logic to route through Freedom Link
    log_freedom_link_traffic(service, request)
    # Rest of the routing logic
    pass

## Summary
- Added logging setup and audit logging function in `logging.py`
- Created function to log Freedom Link traffic in `audit.py`
- Integrated Freedom Link traffic logging in `ai.py`