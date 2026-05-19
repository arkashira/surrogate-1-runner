import os
import subprocess
from utils.diff_parser import parse_diff
from unittest import TestLoader

def get_changed_files():
    """Retrieve files changed between the last commit and HEAD."""
    result = subprocess.run(['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'], capture_output=True, text=True)
    return result.stdout.splitlines()

def filter_tests(changed_files):
    """Filter tests based on changed files."""
    test_cases = []
    for file in changed_files:
        # Assuming a simple mapping where test files are named similarly to the source files they test
        test_file = f"tests/{file.replace('.py', '_test.py')}"
        if os.path.exists(test_file):
            test_cases.append(test_file)
    return test_cases

def execute_filtered_tests(tests):
    """Execute the filtered tests using the unittest framework."""
    test_loader = TestLoader()
    test_suite = test_loader.loadTestsFromNames(tests)
    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suite)

def main():
    changed_files = get_changed_files()
    relevant_tests = filter_tests(changed_files)
    print("Relevant tests to run:", relevant_tests)
    execute_filtered_tests(relevant_tests)

if __name__ == "__main__":
    main()