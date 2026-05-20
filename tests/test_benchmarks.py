import json
import os
import unittest

class TestBenchmarks(unittest.TestCase):
    def test_benchmark_files_exist(self):
        benchmark_dir = '/opt/axentx/surrogate-1/data/benchmarks'
        expected_files = [
            'b2b_saas.json',
            'marketplace.json',
            'ai_tool.json',
            'financial_services.json',
            'healthcare.json'
        ]

        for file_name in expected_files:
            file_path = os.path.join(benchmark_dir, file_name)
            self.assertTrue(os.path.exists(file_path), f"Benchmark file {file_name} does not exist")

    def test_benchmark_files_content(self):
        benchmark_dir = '/opt/axentx/surrogate-1/data/benchmarks'
        expected_files = [
            'b2b_saas.json',
            'marketplace.json',
            'ai_tool.json',
            'financial_services.json',
            'healthcare.json'
        ]

        for file_name in expected_files:
            file_path = os.path.join(benchmark_dir, file_name)
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.assertIn('category', data)
                self.assertIn('metrics', data)
                self.assertIsInstance(data['metrics'], dict)

if __name__ == '__main__':
    unittest.main()