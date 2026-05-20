import os
import requests
import subprocess
from datetime import datetime

class UpdateManager:
    def __init__(self, current_version):
        self.current_version = current_version
        self.latest_version_url = "https://api.github.com/repos/axentx/surrogate-1/releases/latest"

    def check_for_updates(self):
        response = requests.get(self.latest_version_url)
        if response.status_code == 200:
            latest_release = response.json()
            latest_version = latest_release['tag_name']
            if latest_version != self.current_version:
                return latest_version
        return None

    def download_update(self, version):
        download_url = f"https://github.com/axentx/surrogate-1/archive/refs/tags/{version}.tar.gz"
        filename = f"/tmp/surrogate-1-{version}.tar.gz"
        response = requests.get(download_url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            return filename
        return None

    def apply_update(self, filename):
        extract_dir = "/tmp/surrogate-1-update"
        os.makedirs(extract_dir, exist_ok=True)
        subprocess.run(["tar", "-xzf", filename, "-C", extract_dir])
        subprocess.run(["cp", "-r", f"{extract_dir}/surrogate-1-{self.current_version}/.", "/opt/axentx/surrogate-1"])
        subprocess.run(["rm", "-rf", extract_dir, filename])

    def update(self):
        latest_version = self.check_for_updates()
        if latest_version:
            print(f"New version available: {latest_version}")
            filename = self.download_update(latest_version)
            if filename:
                print("Download complete. Applying update...")
                self.apply_update(filename)
                print("Update applied successfully.")
            else:
                print("Failed to download update.")
        else:
            print("No updates available.")

def main():
    current_version = "v1.0.0"  # Replace with actual version checking logic
    updater = UpdateManager(current_version)
    updater.update()

if __name__ == "__main__":
    main()