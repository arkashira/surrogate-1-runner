
import json
import sys

def handle_failure(failure_details):
    failure_json = json.dumps(failure_details)
    print(f'{{"failure_details": {failure_json}}}')
    sys.exit(1)

def main():
    # Your existing code for handling container failures goes here...

    # Assuming you have a function that returns failure details when a critical failure occurs
    if critical_failure_occurred():
        failure_details = get_failure_details()
        handle_failure(failure_details)

if __name__ == "__main__":
    main()