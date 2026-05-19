# <repo_root>/test_configurations/test_filter_tests.py
# -------------------------------------------------
import os
import unittest
from test_configurations.filter_tests import (
    create_env_var_filter,
    get_filtered_tests,
)


class TestEnvironmentVariableFiltering(unittest.TestCase):
    def setUp(self):
        # A deterministic list of dummy test names used by every test case.
        self.test_names = ['TestA', 'TestB', 'TestC']

    def tearDown(self):
        # Clean up any env vars we may have set so tests stay isolated.
        for var in ['TEST_ENV_VAR', 'TEST_ENV_VAR_1', 'TEST_ENV_VAR_2']:
            os.environ.pop(var, None)

    def test_filter_based_on_environment_variable(self):
        os.environ['TEST_ENV_VAR'] = 'testa'
        filter_fn = create_env_var_filter('TEST_ENV_VAR')
        filtered = get_filtered_tests(self.test_names, [filter_fn])

        self.assertIn('TestA', filtered)
        self.assertNotIn('TestB', filtered)
        self.assertNotIn('TestC', filtered)

    def test_case_insensitive_filtering(self):
        os.environ['TEST_ENV_VAR'] = 'TESTA'   # Upper‑case on purpose
        filter_fn = create_env_var_filter('TEST_ENV_VAR')
        filtered = get_filtered_tests(self.test_names, [filter_fn])

        self.assertIn('TestA', filtered)
        self.assertNotIn('TestB', filtered)
        self.assertNotIn('TestC', filtered)

    def test_combined_filtering_criteria(self):
        os.environ['TEST_ENV_VAR_1'] = 'testa'
        os.environ['TEST_ENV_VAR_2'] = 'testb'
        f1 = create_env_var_filter('TEST_ENV_VAR_1')
        f2 = create_env_var_filter('TEST_ENV_VAR_2')
        filtered = get_filtered_tests(self.test_names, [f1, f2])

        # Both filters must be satisfied → only TestA (contains "testa")
        # and TestB (contains "testb") survive because each filter is
        # evaluated independently; the overall result is the intersection.
        self.assertIn('TestA', filtered)
        self.assertIn('TestB', filtered)
        self.assertNotIn('TestC', filtered)

    def test_missing_env_var_means_no_restriction(self):
        # No env var set → filter should behave like a pass‑through.
        filter_fn = create_env_var_filter('NON_EXISTENT_VAR')
        filtered = get_filtered_tests(self.test_names, [filter_fn])
        self.assertCountEqual(filtered, self.test_names)


if __name__ == '__main__':
    unittest.main()