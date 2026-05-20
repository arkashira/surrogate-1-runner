
import json
import os

class ResultStore:
    def __init__(self, results_dir):
        self.results_dir = results_dir
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

    def store_result(self, test_name, result):
        file_path = os.path.join(self.results_dir, f"{test_name}.json")
        with open(file_path, 'w') as f:
            json.dump(result, f, indent=4)

# /opt/axentx/surrogate-1/src/test_harness.py

import os
import json
from result_store import ResultStore

class TestHarness:
    def __init__(self, scripts_dir, results_dir):
        self.scripts_dir = scripts_dir
        self.results_dir = results_dir
        self.result_store = ResultStore(results_dir)

    def run_tests(self):
        # ... (other test running logic)
        # After test execution, store the result in JSON
        self.result_store.store_result(test_name, result)

## Summary
- Implemented `ResultStore` class to store test results in JSON format.
- Modified `TestHarness` class to use `ResultStore` after test execution.
- Test results are stored in JSON files in the specified results directory.