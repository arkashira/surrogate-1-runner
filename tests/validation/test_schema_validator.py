import unittest
import json
from src.validation.schema_validator import SchemaValidator
from src.validation.error_codes import ValidationErrorCode

class TestSchemaValidator(unittest.TestCase):
    """Tests for the SchemaValidator class."""

    def setUp(self):
        """Set up the test case."""
        self.schema_path = 'tests/data/test_schema.json'
        self.validator = SchemaValidator(self.schema_path)

    def test_valid_pair(self):
        """Test validation of a valid training pair."""
        valid_pair = {
            "input": "This is a valid input.",
            "output": "This is a valid output."
        }
        is_valid, error_code, error_message = self.validator.validate_pair(valid_pair)
        self.assertTrue(is_valid)
        self.assertIsNone(error_code)
        self.assertIsNone(error_message)

    def test_missing_required_field(self):
        """Test validation of a training pair with a missing required field."""
        invalid_pair = {
            "output": "This is a valid output."
        }
        is_valid, error_code, error_message = self.validator.validate_pair(invalid_pair)
        self.assertFalse(is_valid)
        self.assertEqual(error_code, ValidationErrorCode.MISSING_REQUIRED_FIELD)
        self.assertIn("'input' is a required property", error_message)

    def test_invalid_field_type(self):
        """Test validation of a training pair with an invalid field type."""
        invalid_pair = {
            "input": 123,
            "output": "This is a valid output."
        }
        is_valid, error_code, error_message = self.validator.validate_pair(invalid_pair)
        self.assertFalse(is_valid)
        self.assertEqual(error_code, ValidationErrorCode.INVALID_FIELD_TYPE)
        self.assertIn("123 is not of type 'string'", error_message)

    def test_invalid_field_value(self):
        """Test validation of a training pair with an invalid field value."""
        invalid_pair = {
            "input": "This is a valid input.",
            "output": "invalid"
        }
        is_valid, error_code, error_message = self.validator.validate_pair(invalid_pair)
        self.assertFalse(is_valid)
        self.assertEqual(error_code, ValidationErrorCode.INVALID_FIELD_VALUE)
        self.assertIn("'invalid' is not one of ['valid']", error_message)

    def test_invalid_field_format(self):
        """Test validation of a training pair with an invalid field format."""
        invalid_pair = {
            "input": "This is a valid input.",
            "output": "This is a valid output.",
            "timestamp": "invalid-date"
        }
        is_valid, error_code, error_message = self.validator.validate_pair(invalid_pair)
        self.assertFalse(is_valid)
        self.assertEqual(error_code, ValidationErrorCode.INVALID_FIELD_FORMAT)
        self.assertIn("'invalid-date' is not a 'date-time'", error_message)

if __name__ == '__main__':
    unittest.main()