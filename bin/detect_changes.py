import subprocess
from typing import List

def get_changed_files() -> List[str]:
    """Detect changed files in the current commit."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
        capture_output=True,
        text=True
    )
    changed_files = result.stdout.splitlines()
    return changed_files

def filter_tests(changed_files: List[str]) -> List[str]:
    """Filter test cases that cover modified code paths."""
    test_files = []
    for file in changed_files:
        if file.endswith(".py"):
            test_file = file.replace(".py", "_test.py")
            test_files.append(test_file)
    return test_files

def exclude_tests(test_files: List[str]) -> None:
    """Exclude filtered tests from execution."""
    for test_file in test_files:
        subprocess.run(["pytest", "--ignore", test_file], check=True)

if __name__ == "__main__":
    changed_files = get_changed_files()
    test_files = filter_tests(changed_files)
    exclude_tests(test_files)