import unittest
from src.pipeline_integration import process_pipeline
from mock_resolver import MockResolver  # Assume a mock resolver is available for testing

class TestPipelineIntegration(unittest.TestCase):
    def setUp(self):
        self.mock_resolver = MockResolver()
        resolver.resolve_tokens = self.mock_resolver.resolve_tokens

    def test_process_pipeline(self):
        test_data = {"tokens": ["token1", "token2"]}
        expected_resolved_data = {"resolved_tokens": ["resolved1", "resolved2"]}
        self.mock_resolver.set_expected_result(expected_resolved_data)

        resolved_data = process_pipeline(test_data)
        self.assertEqual(resolved_data, expected_resolved_data)

if __name__ == '__main__':
    unittest.main()