
import unittest
import json

from src.ci_handler import handle_failure, main

class TestCiHandler(unittest.TestCase):
    def test_handle_failure(self):
        failure_details = {"container_name": "my_container", "error_message": "Critical failure occurred"}
        handle_failure(failure_details)
        output = sys.stdout.getvalue().strip()
        expected_output = '{"failure_details": {"container_name": "my_container", "error_message": "Critical failure occurred"}}'
        self.assertEqual(output, expected_output)

    def test_main(self):
        # Your existing test cases for the main function go here...

        # Test the new exit code handling
        with patch('src.ci_handler.critical_failure_occurred') as mock_critical_failure:
            mock_critical_failure.return_value = True
            main()
            self.assertEqual(sys.exitcode, 1)

if __name__ == "__main__":
    unittest.main()