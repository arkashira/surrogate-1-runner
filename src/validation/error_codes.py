from enum import Enum, auto

class ValidationErrorCode(Enum):
    """Enumeration of validation error codes for training pairs."""

    # Schema validation errors
    MISSING_REQUIRED_FIELD = auto()
    INVALID_FIELD_TYPE = auto()
    INVALID_FIELD_VALUE = auto()
    INVALID_FIELD_FORMAT = auto()

    # Data quality errors
    DUPLICATE_PAIR = auto()
    INCONSISTENT_DATA = auto()
    OUT_OF_RANGE_VALUE = auto()

    # Structural errors
    INVALID_JSON_STRUCTURE = auto()
    MISSING_JSON_ROOT = auto()

    # Custom validation errors
    CUSTOM_VALIDATION_FAILED = auto()

    def __str__(self):
        """Return the name of the error code."""
        return self.name