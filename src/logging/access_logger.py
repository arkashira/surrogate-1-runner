import logging

# Configure logging
logging.basicConfig(
    filename='access.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_unauthorized_access(user_id, action):
    logging.warning(f'Unauthorized access attempt by user {user_id} for action: {action}')