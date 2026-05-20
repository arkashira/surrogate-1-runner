import logging
from pathlib import Path

# Ensure log directory exists
log_dir = Path("/var/log/axentx/surrogate-1")
log_dir.mkdir(parents=True, exist_ok=True)

# Configure logger
logger = logging.getLogger("validation_error_handler")
logger.setLevel(logging.INFO)

# Create file handler
file_handler = logging.FileHandler("/var/log/axentx/surrogate-1/validation.log")
file_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(file_handler)

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

def handle_validation_error(error_message: str, context: dict = None):
    """
    Log validation errors with clear messages and optional context.

    Args:
        error_message (str): Description of the validation failure
        context (dict, optional): Additional information about the error
    """
    full_message = f"Validation Error: {error_message}"
    if context:
        full_message += f" | Context: {context}"
    logger.error(full_message)
    raise ValidationError(full_message)