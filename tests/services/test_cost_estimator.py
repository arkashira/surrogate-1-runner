import unittest
from src.services.cost_estimator import CostEstimator

class TestCostEstimator(unittest.TestCase):
    def setUp(self):
        self.estimator = CostEstimator("gpt-3.5-turbo")

    def test_estimate_cost(self):
        prompt = "Hello, world!"
        cost = self.estimator.estimate_cost(prompt, "gpt-3.5-turbo")
        self.assertIsNotNone(cost)
        self.assertGreater(cost, 0)

    def test_unsupported_model(self):
        cost = self.estimator.estimate_cost("Hello, world!", "unsupported-model")
        self.assertIsNone(cost)

if __name__ == "__main__":
    unittest.main()