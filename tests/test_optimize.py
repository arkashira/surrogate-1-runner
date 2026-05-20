import unittest
from optimize import OptimizedAPI

class TestOptimizedAPI(unittest.TestCase):
    def setUp(self):
        self.api = OptimizedAPI(llm_runtime="local_llm")

    def test_perform_inference(self):
        input_data = {"input": "some_input"}
        result = self.api.perform_inference(input_data)
        self.assertIn("result", result)
        self.assertEqual(result["result"], "inference_result")

if __name__ == "__main__":
    unittest.main()