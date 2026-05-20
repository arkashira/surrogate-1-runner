
import jsonschema
from jsonschema import validate
from typing import Dict, Any, Optional

from .validation_rules import TRAINING_PAIR_SCHEMA

def validate_training_pair(pair: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a training pair against the defined JSON schema.

    Args:
        pair: The training pair dictionary to validate.

    Returns:
        A dictionary with validation result. If valid, returns an empty dict.
        If invalid, returns a dictionary with error details.

    Raises:
        jsonschema.exceptions.ValidationError: If the pair is invalid and strict validation is enabled.
    """
    try:
        validate(instance=pair, schema=TRAINING_PAIR_SCHEMA)
        return {}
    except jsonschema.exceptions.ValidationError as e:
        # Extract detailed error information
        error_details = {
            "error_code": "INVALID_PAIR",
            "message": "Training pair does not conform to the schema.",
            "details": e.message,
            "invalid_fields": e.path
        }
        return error_details

def is_valid_pair(pair: Dict[str, Any]) -> bool:
    """
    Check if a training pair is valid without raising an exception.

    Args:
        pair: The training pair dictionary.

    Returns:
        True if the pair is valid, False otherwise.
    """
    try:
        validate(instance=pair, schema=TRAINING_PAIR_SCHEMA)
        return True
    except jsonschema.exceptions.ValidationError:
        return False