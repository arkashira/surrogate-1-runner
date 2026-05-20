import os
import subprocess
import time
from datetime import datetime, timedelta

def check_for_new_version():
    """Check for a newer version of the runner."""
    try:
        with open('version.txt', 'r') as f:
            current_version = f.read().strip()
        # Simulate checking for a new version (e.g., from Git tags)
        # In production, this would fetch the latest tag from the repo
        new_version = "1.1.0"  # Example new version
        if new_version != current_version:
            return new_version
        return None
    except FileNotFoundError:
        return None

def perform_rolling_update(new_version):
    """Execute a rolling update to the new version."""
    print(f"[{datetime.now()}] Starting rolling update to version {new_version}")
    
    # Step 1: Start new instances with the new version
    subprocess.run(["bash", "start_runners.sh", new_version], check=True)
    
    # Step 2: Wait for new instances to become healthy (e.g., 30 seconds)
    time.sleep(30)
    
    # Step 3: Stop old instances gracefully
    subprocess.run(["bash", "stop_runners.sh"], check=True)
    
    print(f"[{datetime.now()}] Rolling update to version {new_version} completed successfully.")

def main():
    new_version = check_for_new_version()
    if new_version:
        perform_rolling_update(new_version)
    else:
        print("No new version available. Continuing with current version.")

if __name__ == '__main__':
    main()