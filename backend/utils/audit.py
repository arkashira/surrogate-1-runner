import logging
import os
from datetime import datetime

LOG_FILE_PATH = "/var/log/axentx/surrogate-1/profile_changes.log"

def setup_audit_logger():
    if not os.path.exists(os.path.dirname(LOG_FILE_PATH)):
        os.makedirs(os.path.dirname(LOG_FILE_PATH))
    
    logger = logging.getLogger('audit_logger')
    logger.setLevel(logging.INFO)
    
    handler = logging.FileHandler(LOG_FILE_PATH)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger

def log_profile_change(user_id, changes):
    audit_logger = setup_audit_logger()
    message = f"User {user_id} updated profile with changes: {changes}"
    audit_logger.info(message)

# Test function to verify the audit log functionality
def test_log_profile_change():
    test_user_id = "test_user_123"
    test_changes = {"name": "New Name", "bio": "Updated Bio"}
    log_profile_change(test_user_id, test_changes)
    with open(LOG_FILE_PATH, 'r') as file:
        log_content = file.read()
        assert f"User {test_user_id} updated profile with changes: {test_changes}" in log_content

if __name__ == "__main__":
    test_log_profile_change()