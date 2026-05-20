import os
import subprocess
import unittest
from surrogate import DesignManager  # Assuming DesignManager is the main class for managing designs

class TestDesignWorkflows(unittest.TestCase):
    def setUp(self):
        self.manager = DesignManager()

    def test_generate_design_file(self):
        design_file = self.manager.generate_design_file("test_design")
        self.assertIsNotNone(design_file)
        self.assertTrue(design_file.endswith('.design'))

    def test_manage_design_files(self):
        self.manager.add_design_file("test_design.design")
        self.assertIn("test_design.design", self.manager.list_design_files())

    def test_no_java_dependency(self):
        """
        Verify that the Surrogate design workflow runs successfully without any
        Java runtime present. The test unsets JAVA_HOME and executes the CLI in
        dry-run mode, asserting a zero exit code and the absence of Java-related
        error messages.
        """
        # Simulate environment without Java
        os.environ.pop("JAVA_HOME", None)

        # Execute the Surrogate CLI in a mode that should not require Java.
        result = subprocess.run(
            ["surrogate-cli", "generate", "--dry-run"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # The process must exit cleanly.
        self.assertEqual(result.returncode, 0, f"Process failed with exit code {result.returncode}: {result.stderr}")

        # Ensure no Java-related errors appear in stderr.
        self.assertNotIn("java", result.stderr.lower(), f"Unexpected Java error: {result.stderr}")

    def test_design_workflow_execution(self):
        result = self.manager.execute_workflow("test_design")
        self.assertTrue(result.success)

if __name__ == '__main__':
    unittest.main()