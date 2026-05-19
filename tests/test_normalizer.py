import unittest
from src.cloud.normalizer import normalize_cost_data

class TestNormalizer(unittest.TestCase):
    def test_normalize_cost_data(self):
        input_data = [
            {
                "provider": "ProviderA",
                "service": "Service1",
                "resource_id": "res-123",
                "amount_usd": 100.0,
                "timestamp": "2023-01-01T00:00:00Z"
            },
            {
                "provider": "ProviderB",
                "service": "Service2",
                "resource_id": "res-456",
                "amount_usd": 200.0,
                "timestamp": "2023-01-02T00:00:00Z"
            }
        ]
        
        expected_output = [
            {
                "provider": "ProviderA",
                "service": "Service1",
                "resource_id": "res-123",
                "amount_usd": 100.0,
                "timestamp": "2023-01-01T00:00:00Z",
                "schema_version": "1.0"
            },
            {
                "provider": "ProviderB",
                "service": "Service2",
                "resource_id": "res-456",
                "amount_usd": 200.0,
                "timestamp": "2023-01-02T00:00:00Z",
                "schema_version": "1.0"
            }
        ]
        
        normalized_data = normalize_cost_data(input_data)
        self.assertEqual(normalized_data, expected_output)

if __name__ == '__main__':
    unittest.main()