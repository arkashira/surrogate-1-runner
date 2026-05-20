import json
import jsonschema
from pathlib import Path
from typing import Dict, Any
from .error_handler import handle_validation_error

# Define the expected schema for training pairs
TRAINING_PAIR_SCHEMA = {
    "type": "object",
    "properties": {
        "input": {"type": "string"},
        "output": {"type": "string"},
        "metadata": {
            "type": "object",
            "properties": {
                "source": {"type": "string"},
                "timestamp": {"type": "string", "format": "date-time"}
            },
            "required": ["source"]
        }
    },
    "required": ["input", "output"]
}

def validate_training_pair(data: Dict[str, Any]) -> bool:
    """
    Validate that the provided data conforms to the expected training pair schema.

    Args:
        data (Dict[str, Any]): Training pair data to validate

    Returns:
        bool: True if valid, raises ValidationError otherwise

    Raises:
        ValidationError: If data doesn't conform to schema
    """
    try:
        jsonschema.validate(instance=data, schema=TRAINING_PAIR_SCHEMA)
        return True
    except jsonschema.exceptions.ValidationError as e:
        handle_validation_error(
            error_message=f"Schema validation failed: {e.message}",
            context={
                "instance": data,
                "path": list(e.absolute_path),
                "validator": e.validator,
                "validator_value": e.validator_value
            }
        )