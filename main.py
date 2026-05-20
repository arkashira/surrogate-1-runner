from logging import getLogger
from access_logger import access_logger

def handle_shell_access(user, session_id, ip_address):
    # Original shell handling logic...
    
    # Log access event
    access_logger.info(
        "Shell session initiated",
        extra={
            'user': user,
            'session_id': session_id,
            'action': 'shell_access',
            'ip': ip_address
        }
    )
    
    # Continue with session establishment