import unittest
from orchestrator import Orchestrator

class TestOrchestrator(unittest.TestCase):
    def setUp(self):
        self.providers = [
            lambda x: f"response_{hashlib.sha256(x.encode()).hexdigest()}",
            lambda x: f"alternative_{hashlib.sha256(x.encode()).hexdigest()}"
        ]
        self.orchestrator = Orchestrator(self.providers)

    def test_deterministic_order(self):
        requests = ["request1", "request2"]
        responses = self.orchestrator.execute_calls(requests)
        expected_responses = [
            f"response_{hashlib.sha256('request1'.encode()).hexdigest()}",
            f"response_{hashlib.sha256('request2'.encode()).hexdigest()}"
        ]
        self.assertEqual(responses, expected_responses)

if __name__ == '__main__':
    unittest.main()