import subprocess
from typing import List, Dict, Set

def get_changed_files() -> Set[str]:
    """Get the set of changed files from the last commit."""
    result = subprocess.run(['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'], capture_output=True, text=True)
    return set(result.stdout.splitlines())

def get_test_cases_for_file(file_path: str) -> List[str]:
    """Get the list of test cases related to a specific file."""
    # This is a placeholder. In a real implementation, you would parse the test files
    # or use a test mapping file to find test cases related to the given file.
    test_cases = []
    if file_path.endswith('.py'):
        test_cases.append(f'test_{file_path.replace(".py", "")}')
    return test_cases

def filter_test_cases(changed_files: Set[str]) -> List[str]:
    """Filter test cases based on changed files."""
    filtered_test_cases = []
    for file_path in changed_files:
        filtered_test_cases.extend(get_test_cases_for_file(file_path))
    return filtered_test_cases

def main():
    changed_files = get_changed_files()
    filtered_test_cases = filter_test_cases(changed_files)
    print("Filtered test cases:", filtered_test_cases)

if __name__ == "__main__":
    main()