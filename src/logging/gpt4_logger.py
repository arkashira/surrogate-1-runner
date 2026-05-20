import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='/opt/axentx/surrogate-1/logs/gpt4_usage.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_gpt4_usage(user_id, action):
    """Log the usage of GPT-4 by a user."""
    logging.info(f'User: {user_id}, Action: {action}')

def log_error(user_id, error_message):
    """Log errors related to GPT-4 usage."""
    logging.error(f'User: {user_id}, Error: {error_message}')