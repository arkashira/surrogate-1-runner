import unittest
from src.priority_calculator import PriorityCalculator

class TestPriorityCalculator(unittest.TestCase):
    def setUp(self):
        self.coverage_gaps = {"test_case_1": 0.5, "test_case_2": 0.3, "test_case_3": 0.2}
        self.change_impact = {"test_case_1": 0.8, "test_case_2": 0.4, "test_case_3": 0.1}
        self.calculator = PriorityCalculator(self.coverage_gaps, self.change_impact)

    def test_calculate_priority(self):
        test_cases = ["test_case_1", "test_case_2", "test_case_3"]
        prioritized_test_cases = self.calculator.calculate_priority(test_cases)
        expected = [('test_case_1', 1.3), ('test_case_2', 0.7), ('test_case_3', 0.3)]
        self.assertEqual(prioritized_test_cases, expected)

    def test_filter_test_cases(self):
        changed_files = ["file_1", "file_2"]
        test_cases = ["test_case_1", "test_case_2", "test_case_3"]
        filtered_test_cases = self.calculator.filter_test_cases(changed_files, test_cases)
        expected = [('test_case_1', 1.3), ('test_case_2', 0.7), ('test_case_3', 0.3)]
        self.assertEqual(filtered_test_cases, expected)

if __name__ == "__main__":
    unittest.main()