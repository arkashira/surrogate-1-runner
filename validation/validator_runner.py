from validation.schema_validator import SchemaValidator
from validation.logger import setup_logger, log_error

LOG_FILE = '/var/log/axentx/surrogate-1/validation.log'
SCHEMA_PATH = '/path/to/schema.json'

def main():
    validator = SchemaValidator(SCHEMA_PATH)
    logger = setup_logger(LOG_FILE)
    
    # Example instance for validation
    instance = {
        "key": "value"
    }
    
    error_message = validator.validate(instance)
    if error_message:
        log_error(logger, error_message)
        print(f"Validation failed: {error_message}")
    else:
        print("Validation successful")

if __name__ == "__main__":
    main()