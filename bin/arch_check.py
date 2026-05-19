import subprocess
import argparse
import sys

def calculate_complexity(file_path):
    try:
        result = subprocess.run(['radon', 'cc', file_path], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error calculating complexity for {file_path}: {result.stderr}")
            return None
        return result.stdout
    except Exception as e:
        print(f"Exception occurred while calculating complexity for {file_path}: {e}")
        return None

def check_complexity(file_path, threshold=15):
    complexity_output = calculate_complexity(file_path)
    if complexity_output is None:
        return False

    lines = complexity_output.split('\n')
    for line in lines:
        if 'CC' in line:
            parts = line.split()
            complexity = int(parts[1])
            if complexity > threshold:
                print(f"Complexity check failed for {file_path}: {complexity} > {threshold}")
                return False
    return True

def main():
    parser = argparse.ArgumentParser(description='Check code complexity using radon.')
    parser.add_argument('file_path', help='Path to the file to check')
    parser.add_argument('--threshold', type=int, default=15, help='Complexity threshold')
    args = parser.parse_args()

    if not check_complexity(args.file_path, args.threshold):
        sys.exit(1)

if __name__ == '__main__':
    main()