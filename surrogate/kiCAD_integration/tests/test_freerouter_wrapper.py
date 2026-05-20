import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from freerouter_wrapper import FreerouterWrapper
import subprocess

class TestFreerouterWrapper(unittest.TestCase):
    @patch('freerouter_wrapper.subprocess.run')
    def test_run_success(self, mock_run):
        # Setup
        wrapper = FreerouterWrapper(kicad_version="9")
        input_file = "test_input.kicad_pcb"
        output_file = "test_output.kicad_pcb"

        # Create mock files
        Path(input_file).touch()
        Path(output_file).touch()

        # Mock subprocess.run to return successfully
        mock_run.return_value = MagicMock()

        # Execute
        wrapper.run(input_file, output_file)

        # Assert
        mock_run.assert_called_once_with(
            ["/usr/local/bin/freerouter9", "--input", input_file, "--output", output_file],
            check=True
        )

    @patch('freerouter_wrapper.subprocess.run')
    def test_run_failure(self, mock_run):
        # Setup
        wrapper = FreerouterWrapper(kicad_version="9")
        input_file = "test_input.kicad_pcb"
        output_file = "test_output.kicad_pcb"

        # Mock subprocess.run to raise an exception
        mock_run.side_effect = subprocess.CalledProcessError(1, [])

        # Execute and assert
        with self.assertRaises(SystemExit) as cm:
            wrapper.run(input_file, output_file)
        self.assertEqual(cm.exception.code, 1)

    def test_get_freerouter_path(self):
        # Setup
        wrapper = FreerouterWrapper(kicad_version="9")

        # Execute
        path = wrapper._get_freerouter_path()

        # Assert
        self.assertEqual(path, "/usr/local/bin/freerouter9")

    def test_get_freerouter_path_unsupported_version(self):
        # Setup
        wrapper = FreerouterWrapper(kicad_version="8")

        # Execute and assert
        with self.assertRaises(ValueError):
            wrapper._get_freerouter_path()

if __name__ == "__main__":
    unittest.main()