import json
import pathlib
import unittest

from jsonschema import Draft7Validator, ValidationError

SCHEMA_PATH = pathlib.Path(__file__).resolve().parents[1] / "src" / "models" / "operating_mode_schema.json"


def load_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# Three real‑world sample payloads (simplified for illustration)
SAMPLE_PAYLOADS = [
    {
        "LN0": {"mode": "automatic", "status": True, "timestamp": "2023-01-01T00:00:00Z"},
        "LN1": {"mode": "manual", "status": False, "timestamp": "2023-01-01T00:01:00Z"},
        "LN2": {"mode": "standby", "status": True, "timestamp": "2023-01-01T00:02:00Z"},
        "LN3": {"mode": "automatic", "status": True, "timestamp": "2023-01-01T00:03:00Z"},
        "LN4": {"mode": "manual", "status": False, "timestamp": "2023-01-01T00:04:00Z"},
        "LN5": {"mode": "standby", "status": True, "timestamp": "2023-01-01T00:05:00Z"},
        "LN6": {"mode": "automatic", "status": True, "timestamp": "2023-01-01T00:06:00Z"},
        "LN7": {"mode": "manual", "status": False, "timestamp": "2023-01-01T00:07:00Z"},
        "LN8": {"mode": "standby", "status": True, "timestamp": "2023-01-01T00:08:00Z"},
        "LN9": {"mode": "automatic", "status": True, "timestamp": "2023-01-01T00:09:00Z"},
    },
    {
        "LN0": {"mode": "manual", "status": False, "timestamp": "2023-06-15T12:00:00Z"},
        "LN1": {"mode": "manual", "status": False, "timestamp": "2023-06-15T12:01:00Z"},
        "LN2": {"mode": "manual", "status": False, "timestamp": "2023-06-15T12:02:00Z"},
        "LN3": {"mode": "manual", "status": False, "timestamp": "2023-06-15T12:03:00Z"},
        "LN4": {"mode": "manual", "status": False, "timestamp": "2023-06-15T12:04:00Z"},
        "LN5": {"mode": "manual", "status": False, "timestamp": "2023-06-15T12:05:00Z"},
        "LN6": {"mode": "manual", "status": False, "timestamp": "2023-06-15T12:06:00Z"},
        "LN7": {"mode": "manual", "status": False, "timestamp": "2023-06-15T12:07:00Z"},
        "LN8": {"mode": "manual", "status": False, "timestamp": "2023-06-15T12:08:00Z"},
        "LN9": {"mode": "manual", "status": False, "timestamp": "2023-06-15T12:09:00Z"},
    },
    {
        "LN0": {"mode": "standby", "status": True, "timestamp": "2024-03-20T08:30:00Z"},
        "LN1": {"mode": "standby", "status": True, "timestamp": "2024-03-20T08:31:00Z"},
        "LN2": {"mode": "standby", "status": True, "timestamp": "2024-03-20T08:32:00Z"},
        "LN3": {"mode": "standby", "status": True, "timestamp": "2024-03-20T08:33:00Z"},
        "LN4": {"mode": "standby", "status": True, "timestamp": "2024-03-20T08:34:00Z"},
        "LN5": {"mode": "standby", "status": True, "timestamp": "2024-03-20T08:35:00Z"},
        "LN6": {"mode": "standby", "status": True, "timestamp": "2024-03-20T08:36:00Z"},
        "LN7": {"mode": "standby", "status": True, "timestamp": "2024-03-20T08:37:00Z"},
        "LN8": {"mode": "standby", "status": True, "timestamp": "2024-03-20T08:38:00Z"},
        "LN9": {"mode": "standby", "status": True, "timestamp": "2024-03-20T08:39:00Z"},
    },
]


class TestOperatingModeSchema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = load_schema()
        cls.validator = Draft7Validator(cls.schema)

    def test_valid_payloads(self):
        """All provided sample payloads must validate against the schema."""
        for idx, payload in enumerate(SAMPLE_PAYLOADS, start=1):
            with self.subTest(payload=idx):
                errors = sorted(self.validator.iter_errors(payload), key=lambda e: e.path)
                self.assertEqual(
                    errors,
                    [],
                    msg=f"Payload {idx} failed validation: {[e.message for e in errors]}",
                )

    def test_invalid_payload_missing_node(self):
        """A payload missing a required logical node should be rejected."""
        invalid = SAMPLE_PAYLOADS[0].copy()
        del invalid["LN5"]  # remove required node
        with self.assertRaises(ValidationError):
            self.validator.validate(invalid)


if __name__ == "__main__":
    unittest.main()