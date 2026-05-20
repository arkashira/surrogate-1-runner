import subprocess
import os
import sys
from pathlib import Path

class FreerouterWrapper:
    def __init__(self, kicad_version="9"):
        self.kicad_version = kicad_version
        self.freerouter_path = self._get_freerouter_path()

    def _get_freerouter_path(self):
        # Determine the correct freerouter path based on KiCAD version
        if self.kicad_version == "9":
            return "/usr/local/bin/freerouter9"
        else:
            raise ValueError(f"Unsupported KiCAD version: {self.kicad_version}")

    def run(self, input_file, output_file):
        try:
            # Check if input file exists
            if not Path(input_file).exists():
                raise FileNotFoundError(f"Input file {input_file} not found")

            # Run freerouter with the appropriate command
            command = [
                self.freerouter_path,
                "--input", input_file,
                "--output", output_file
            ]

            subprocess.run(command, check=True)
            print(f"Successfully ran freerouter on {input_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error running freerouter: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python freerouter_wrapper.py <kicad_version> <input_file> <output_file>")
        sys.exit(1)

    kicad_version = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    wrapper = FreerouterWrapper(kicad_version)
    wrapper.run(input_file, output_file)