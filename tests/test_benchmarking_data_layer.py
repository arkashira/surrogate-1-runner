import unittest
import pandas as pd
from src.benchmarking.data_layer import BenchmarkingDataLayer

class TestBenchmarkingDataLayer(unittest.TestCase):
    def setUp(self):
        self.benchmarking_data_layer = BenchmarkingDataLayer()
        self.test_data = {
            "burn_rate": 100000,
            "traction": 5000,
            "pmf_score": 75
        }
        self.test_benchmark_data = pd.DataFrame({
            "burn_rate": [90000, 110000, 100000],
            "traction": [4000, 6000, 5000],
            "pmf_score": [70, 80, 75]
        })

    def test_load_benchmark_data(self):
        self.benchmarking_data_layer.load_benchmark_data("tests/test_benchmark_data.csv")
        self.assertFalse(self.benchmarking_data_layer.benchmark_data.empty)

    def test_get_benchmark_data(self):
        self.benchmarking_data_layer.benchmark_data = self.test_benchmark_data
        benchmark_data = self.benchmarking_data_layer.get_benchmark_data()
        self.assertEqual(benchmark_data.equals(self.test_benchmark_data), True)

    def test_compare_with_benchmarks(self):
        self.benchmarking_data_layer.benchmark_data = self.test_benchmark_data
        comparison = self.benchmarking_data_layer.compare_with_benchmarks(self.test_data)
        expected_comparison = {
            "burn_rate": 100000 - 100000,
            "traction": 5000 - 5000,
            "pmf_score": 75 - 75
        }
        self.assertEqual(comparison, expected_comparison)

    def test_get_benchmark_comparison(self):
        self.benchmarking_data_layer.benchmark_data = self.test_benchmark_data
        comparison = self.benchmarking_data_layer.get_benchmark_comparison(self.test_data)
        expected_comparison = {
            "burn_rate": 100000 - 100000,
            "traction": 5000 - 5000,
            "pmf_score": 75 - 75
        }
        self.assertEqual(comparison, expected_comparison)

    def test_save_comparison_to_csv(self):
        comparison = {
            "burn_rate": 100000 - 100000,
            "traction": 5000 - 5000,
            "pmf_score": 75 - 75
        }
        self.benchmarking_data_layer.save_comparison_to_csv(comparison, "tests/test_comparison.csv")
        saved_comparison = pd.read_csv("tests/test_comparison.csv")
        self.assertEqual(saved_comparison.to_dict('records')[0], comparison)

    def test_save_comparison_to_pdf(self):
        comparison = {
            "burn_rate": 100000 - 100000,
            "traction": 5000 - 5000,
            "pmf_score": 75 - 75
        }
        self.benchmarking_data_layer.save_comparison_to_pdf(comparison, "tests/test_comparison.pdf")
        # Note: PDF content verification is not straightforward, so we just check if the file is created.
        import os
        self.assertTrue(os.path.exists("tests/test_comparison.pdf"))

if __name__ == "__main__":
    unittest.main()