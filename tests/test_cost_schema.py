import unittest
import os
import json
from src.models.cost_schema import CostSchema

class TestCostSchema(unittest.TestCase):
    def setUp(self):
        self.record = {
            "provider": "aws",
            "service": "s3",
            "resource_id": "res123",
            "amount_usd": 100.0,
            "timestamp": "2023-01-01T00:00:00Z"
        }
        self.test_file = "test_cost_data.json"
        # Create test file
        with open(self.test_file, 'w') as f:
            json.dump(self.record, f)

    def tearDown(self):
        # Clean up test file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_normalize_record(self):
        normalized_record = CostSchema.normalize_record(self.record)
        self.assertEqual(normalized_record["provider"], "aws")
        self.assertEqual(normalized_record["service"], "s3")
        self.assertEqual(normalized_record["resource_id"], "res123")
        self.assertEqual(normalized_record["amount_usd"], 100.0)
        self.assertEqual(normalized_record["timestamp"], "2023-01-01T00:00:00Z")
        self.assertEqual(normalized_record["schema_version"], "1.0")

    def test_normalize_missing_fields(self):
        incomplete_record = {"provider": "gcp"}  # Missing other fields
        normalized = CostSchema.normalize_record(incomplete_record)
        self.assertEqual(normalized["provider"], "gcp")
        self.assertEqual(normalized["service"], "")
        self.assertEqual(normalized["amount_usd"], 0.0)
        self.assertEqual(normalized["schema_version"], "1.0")

    def test_validate_record(self):
        normalized_record = CostSchema.normalize_record(self.record)
        self.assertTrue(CostSchema.validate_record(normalized_record))
        
        # Test invalid record
        invalid_record = {"provider": "aws"}  # Missing required fields
        self.assertFalse(CostSchema.validate_record(invalid_record))

    def test_load_cost_data(self):
        loaded_record = CostSchema.load_cost_data(self.test_file)
        self.assertEqual(loaded_record["provider"], "aws")
        self.assertEqual(loaded_record["schema_version"], "1.0")
        self.assertTrue(CostSchema.validate_record(loaded_record))

if __name__ == '__main__':
    unittest.main()