import os
import subprocess

def run_freerouter(command):
    try:
        # Use subprocess to run the command without Java dependency
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Freerouter: {e}")

def main():
    # Replace Java dependency with alternative solution
    command = "freerouter --no-java"
    run_freerouter(command)

if __name__ == "__main__":
    main()