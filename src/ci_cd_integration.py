from test_filter import get_changed_files, filter_test_cases

def display_filtered_test_cases():
    changed_files = get_changed_files()
    filtered_test_cases = filter_test_cases(changed_files)
    print("Filtered test cases for CI/CD pipeline:")
    for test_case in filtered_test_cases:
        print(test_case)

if __name__ == "__main__":
    display_filtered_test_cases()