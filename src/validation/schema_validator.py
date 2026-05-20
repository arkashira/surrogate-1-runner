import json
from jsonschema import validate, ValidationError
from .error_codes import ValidationErrorCode

class SchemaValidator:
    """Validator for training pairs against a JSON schema."""

    def __init__(self, schema_path):
        """Initialize the validator with the given schema path."""
        with open(schema_path, 'r') as schema_file:
            self.schema = json.load(schema_file)

    def validate_pair(self, training_pair):
        """Validate a training pair against the schema.

        Args:
            training_pair: The training pair to validate.

        Returns:
            A tuple of (is_valid, error_code, error_message).
        """
        try:
            validate(instance=training_pair, schema=self.schema)
            return (True, None, None)
        except ValidationError as e:
            error_code = self._map_validation_error(e)
            return (False, error_code, str(e))

    def _map_validation_error(self, validation_error):
        """Map a jsonschema ValidationError to a ValidationErrorCode."""
        if validation_error.validator == 'required':
            return ValidationErrorCode.MISSING_REQUIRED_FIELD
        elif validation_error.validator == 'type':
            return ValidationErrorCode.INVALID_FIELD_TYPE
        elif validation_error.validator == 'enum':
            return ValidationErrorCode.INVALID_FIELD_VALUE
        elif validation_error.validator == 'format':
            return ValidationErrorCode.INVALID_FIELD_FORMAT
        else:
            return ValidationErrorCode.CUSTOM_VALIDATION_FAILED