import os
import logging
from typing import List, Dict, Tuple

class PriorityCalculator:
    def __init__(self, coverage_gaps: Dict[str, float], change_impact: Dict[str, float]):
        """
        Initialize the priority calculator with coverage gaps and change impact.

        Args:
        - coverage_gaps (Dict[str, float]): A dictionary of coverage gaps where the key is the test case and the value is the gap severity.
        - change_impact (Dict[str, float]): A dictionary of change impact where the key is the test case and the value is the impact severity.
        """
        self.coverage_gaps = coverage_gaps
        self.change_impact = change_impact

    def calculate_priority(self, test_cases: List[str]) -> List[Tuple[str, float]]:
        """
        Calculate the priority of test cases based on coverage gap severity and change impact.

        Args:
        - test_cases (List[str]): A list of test cases.

        Returns:
        - A list of prioritized test cases with their respective priorities.
        """
        prioritized_test_cases = []
        for test_case in test_cases:
            coverage_gap = self.coverage_gaps.get(test_case, 0)
            change_impact_value = self.change_impact.get(test_case, 0)
            priority = coverage_gap + change_impact_value
            prioritized_test_cases.append((test_case, priority))
        prioritized_test_cases.sort(key=lambda x: x[1], reverse=True)
        return prioritized_test_cases

    def filter_test_cases(self, changed_files: List[str], test_cases: List[str]) -> List[Tuple[str, float]]:
        """
        Filter test cases based on changed files and priority.

        Args:
        - changed_files (List[str]): A list of changed files.
        - test_cases (List[str]): A list of test cases.

        Returns:
        - A list of filtered and prioritized test cases with their respective priorities.
        """
        # Filter test cases that are related to changed files
        related_test_cases = [test_case for test_case in test_cases if any(changed_file in test_case for changed_file in changed_files)]
        # Calculate priority and filter test cases
        prioritized_test_cases = self.calculate_priority(related_test_cases)
        return prioritized_test_cases

def main():
    # Example usage
    coverage_gaps = {"test_case_1": 0.5, "test_case_2": 0.3, "test_case_3": 0.2}
    change_impact = {"test_case_1": 0.8, "test_case_2": 0.4, "test_case_3": 0.1}
    calculator = PriorityCalculator(coverage_gaps, change_impact)
    changed_files = ["file_1", "file_2"]
    test_cases = ["test_case_1", "test_case_2", "test_case_3"]
    filtered_test_cases = calculator.filter_test_cases(changed_files, test_cases)
    print(filtered_test_cases)

if __name__ == "__main__":
    main()