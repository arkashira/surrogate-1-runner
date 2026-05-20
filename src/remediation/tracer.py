import logging
from datetime import datetime

# Initialize logger from config
logger = logging.getLogger('surrogate1')

def log_action(action_type, pod_name, status, details=None):
    """
    Logs an action execution with timestamp and details.
    
    Args:
        action_type (str): Type of action (e.g., 'restart', 'rollout', 'config_change')
        pod_name (str): Name of the pod being acted upon
        status (str): Status of the action (e.g., 'success', 'failed', 'in_progress')
        details (dict, optional): Additional details about the action
    """
    timestamp = datetime.now().isoformat()
    log_entry = {
        'timestamp': timestamp,
        'action_type': action_type,
        'pod_name': pod_name,
        'status': status,
        'details': details or {}
    }
    logger.info(f"Action executed: {log_entry}")