
import os
import subprocess

def generate_design_files():
    # Define the design file generation command
    cmd = ["design_generation_tool", "--input", "/path/to/input_file", "--output", "/path/to/output_dir"]

    try:
        # Run the command and capture the output
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        print(f"Design files generated successfully:\n{output.decode()}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating design files: {e.output.decode()}")

# Test the function
generate_design_files()