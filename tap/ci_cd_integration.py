import subprocess
import os
import sys

def get_changed_files():
    """Return a list of files changed in the commit."""
    try:
        output = subprocess.check_output([
            'git', 'diff', '--name-only', '--diff-filter=ACM', 'HEAD^'
        ], stderr=subprocess.PIPE)
        return output.decode().splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving changed files: {e.stderr.decode()}", file=sys.stderr)
        return []

def filter_test_files(changed_files):
    """Identify test files from changed files."""
    test_extensions = ['.test.py', '.py']
    test_prefixes = ['test_']
    test_files = [
        f for f in changed_files
        if any(f.endswith(ext) for ext in test_extensions) or any(f.startswith(p) for p in test_prefixes)
    ]
    return test_files

def run_tests(test_files):
    """Execute pytest on filtered test files."""
    if not test_files:
        print("No test files changed. Skipping test execution.")
        return 0
    
    # Run pytest with only the relevant test files
    cmd = ['pytest'] + test_files
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Test execution failed:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return 1
    return 0

def main():
    changed_files = get_changed_files()
    test_files = filter_test_files(changed_files)
    return run_tests(test_files)

if __name__ == '__main__':
    sys.exit(main())