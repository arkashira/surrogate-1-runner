
import unittest
from src.design_file_generation import generate_design_files

class TestDesignFileGeneration(unittest.TestCase):

    def test_generate_design_files(self):
        # Mock the subprocess module to simulate successful design file generation
        import subprocess
        subprocess.check_output = lambda cmd, **kwargs: b"Design files generated successfully"

        # Call the function to generate design files
        generate_design_files()

        # Assert that the function call did not raise an exception
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()