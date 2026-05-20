import os
import ctypes

def run_freerouter_native():
    try:
        # Load native library
        lib = ctypes.CDLL("./freerouter_native.so")
        # Run Freerouter native
        lib.run_freerouter()
    except OSError as e:
        print(f"Error running Freerouter native: {e}")

def main():
    run_freerouter_native()

if __name__ == "__main__":
    main()