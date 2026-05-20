
import logging
from datetime import datetime

class AccessLogger:
    def __init__(self, log_file='access.log'):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_access_request(self, user, model):
        message = f"Access requested by {user} for model {model} at {datetime.now()}"
        self.logger.info(message)

# /opt/axentx/surrogate-1/gateway.py

# ... (other imports and code)

class Gateway:
    # ... (other methods)

    def access_model(self, user, model):
        # ... (access logic)

        # Log the access request
        self.logger.log_access_request(user, model)

        # ... (rest of the method)

# /opt/axentx/surrogate-1/tests/test_gateway.py

# ... (other imports and test cases)

def test_access_model_logging(mocker):
    logger_mock = mocker.patch('surrogate_1.gateway.AccessLogger')
    gateway = Gateway()
    gateway.access_model('test_user', 'test_model')
    logger_mock.return_value.log_access_request.assert_called_once_with('test_user', 'test_model')

## Summary
- Added `AccessLogger` class to handle logging of access requests
- Modified `Gateway` class to log access requests using the new logger
- Added a test case to verify that access requests are logged correctly