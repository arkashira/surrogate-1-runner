import unittest
from orchestrator import Provider, Orchestrator

class TestOrchestrator(unittest.TestCase):
    def setUp(self):
        self.providers = [
            Provider("ProviderA"),
            Provider("ProviderB"),
            Provider("ProviderC")
        ]
        self.orchestrator = Orchestrator(self.providers)

    def test_load_balance_requests(self):
        requests = ["Request1", "Request2", "Request3"]
        responses = self.orchestrator.load_balance_requests(requests)
        self.assertEqual(len(responses), len(requests))
        for response in responses:
            self.assertTrue(response.startswith("Processed by"))

    def test_failover(self):
        self.providers[0].available = False
        request = "TestRequest"
        response = self.orchestrator.process_request(request)
        self.assertTrue(response.startswith("Processed by"))
        self.assertNotIn("ProviderA", response)

if __name__ == '__main__':
    unittest.main()