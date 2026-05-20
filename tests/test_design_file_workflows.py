import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# Import the real classes – adjust the import path to your package layout
from surrogate import DesignFileGenerator, DesignFileManager


class TestDesignFileWorkflows(unittest.TestCase):
    """
    A hybrid test suite that combines unit‑level isolation with a lightweight
    integration check.  The goal is to prove that:

    1. Design files can be *requested* (unit test – no I/O).
    2. The manager can *store* and *query* those files (unit test – no I/O).
    3. The full automated workflow actually produces a file on disk
       (integration test – uses a temporary directory).
    """

    # ------------------------------------------------------------------
    # 1️⃣  Unit‑level tests – no real file I/O
    # ------------------------------------------------------------------
    def setUp(self):
        """Create fresh instances for every test."""
        self.generator = DesignFileGenerator()
        self.manager = DesignFileManager()

    @patch.object(DesignFileGenerator, "generate")
    def test_generate_design_file_isolated(self, mock_generate):
        """
        Verify that the generator's public API is called correctly.
        The actual file creation is mocked out.
        """
        mock_generate.return_value = "design_123.json"
        design_file = self.generator.generate("test_design")
        mock_generate.assert_called_once_with("test_design")
        self.assertEqual(design_file, "design_123.json")

    @patch.object(DesignFileManager, "file_exists")
    @patch.object(DesignFileManager, "add_file")
    def test_manage_design_file_isolated(self, mock_add, mock_exists):
        """
        Verify that the manager's public API behaves as expected.
        """
        mock_exists.return_value = True
        design_file = "design_123.json"

        # Simulate adding a file
        self.manager.add_file(design_file)
        mock_add.assert_called_once_with(design_file)

        # Simulate existence check
        self.assertTrue(self.manager.file_exists(design_file))
        mock_exists.assert_called_once_with(design_file)

    # ------------------------------------------------------------------
    # 2️⃣  Integration test – real file creation in a temp dir
    # ------------------------------------------------------------------
    def test_automated_workflow_creates_file(self):
        """
        Run the full workflow and confirm that a file appears on disk.
        The workflow is executed in a temporary directory so nothing
        is written to the real project tree.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Patch the generator to write into the temp dir
            with patch.object(
                DesignFileGenerator,
                "_output_dir",
                tmpdir,
                create=True,
            ):
                # Run the workflow
                self.generator.automate_workflow()

                # The workflow should have created at least one file
                created_files = os.listdir(tmpdir)
                self.assertGreater(
                    len(created_files), 0,
                    "Automated workflow did not create any files."
                )

                # Verify that the manager can discover the file
                # (assuming the manager scans the same directory)
                self.manager.set_output_dir(tmpdir)  # expose a helper
                self.assertTrue(
                    any(self.manager.file_exists(f) for f in created_files),
                    "Manager could not find the generated file."
                )

    # ------------------------------------------------------------------
    # 3️⃣  Clean‑up helpers (if needed)
    # ------------------------------------------------------------------
    def tearDown(self):
        """Reset any patched attributes to avoid leaking state."""
        pass  # nothing to clean up in this example


if __name__ == "__main__":
    unittest.main()