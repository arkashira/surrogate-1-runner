import time
from typing import List, Dict, Tuple
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class TestCase:
    id: str
    name: str
    coverage: int  # Number of lines covered
    priority_score: float = 0.0

def calculate_total_coverage(test_cases: List[TestCase]) -> int:
    """
    Calculate the total coverage of all test cases.

    Args:
        test_cases: List of test cases with their coverage metrics

    Returns:
        Total lines of code covered by all tests
    """
    return sum(case.coverage for case in test_cases)

def prioritize_test_cases(test_cases: List[TestCase], total_coverage: int) -> List[TestCase]:
    """
    Prioritize test cases based on coverage gaps.

    Args:
        test_cases: List of test cases with their coverage metrics
        total_coverage: Total lines of code covered by all tests

    Returns:
        List of test cases sorted by priority score (highest first)
    """
    if not test_cases:
        return []

    # Calculate priority scores based on coverage gaps
    for case in test_cases:
        # Priority is inversely proportional to existing coverage
        # Higher priority for test cases covering less-covered areas
        coverage_ratio = case.coverage / max(total_coverage, 1)  # Avoid division by zero
        # Score = (1 - coverage_ratio) * 100 for better prioritization
        case.priority_score = (1 - coverage_ratio) * 100

    # Sort by priority score descending
    return sorted(test_cases, key=lambda x: x.priority_score, reverse=True)

def calculate_coverage_gaps(test_cases: List[TestCase]) -> Dict[str, int]:
    """
    Calculate coverage gaps for each test case.

    Args:
        test_cases: List of test cases with coverage metrics

    Returns:
        Dictionary mapping test case IDs to their coverage gaps
    """
    total_coverage = calculate_total_coverage(test_cases)

    return {case.id: 100 - (case.coverage / max(total_coverage, 1) * 100) for case in test_cases}

def main():
    """Main function to demonstrate test prioritization."""
    # Sample test cases with coverage information
    test_cases = [
        TestCase("TC001", "Login Functionality", 150),
        TestCase("TC002", "User Registration", 80),
        TestCase("TC003", "Data Validation", 200),
        TestCase("TC004", "API Endpoints", 120),
        TestCase("TC005", "Error Handling", 60),
    ]

    start_time = time.time()

    # Prioritize test cases
    prioritized_cases = prioritize_test_cases(test_cases, calculate_total_coverage(test_cases))

    # Calculate coverage gaps
    gaps = calculate_coverage_gaps(test_cases)

    end_time = time.time()

    print("Test Case Prioritization Results:")
    print("-" * 40)
    for i, case in enumerate(prioritized_cases, 1):
        print(f"{i}. {case.name} (ID: {case.id})")
        print(f"   Coverage: {case.coverage} lines")
        print(f"   Priority Score: {case.priority_score:.2f}")
        print(f"   Coverage Gap: {gaps[case.id]:.2f}%")
        print()

    processing_time = end_time - start_time
    print(f"Processing completed in {processing_time:.4f} seconds")

    # Verify it meets time constraint (adjust the limit as needed)
    assert processing_time <= 5.0, f"Processing took {processing_time:.4f}s, exceeds 5s limit"

if __name__ == "__main__":
    main()