import sys
import subprocess
import json
from pathlib import Path

class CrossPlatformShell:
    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = json.load(f)
        self.platform = self._detect_platform()
        self.config = self._apply_platform_config(self.config)
    
    def _detect_platform(self):
        return sys.platform.lower()
    
    def _apply_platform_config(self, config):
        if self.platform in config.get("platforms", {}):
            return {**config, **config["platforms"][self.platform]}
        return config
    
    def execute_command(self, command: str) -> str:
        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"

# Example usage
if __name__ == "__main__":
    shell = CrossPlatformShell("/opt/axentx/surrogate-1/src/config/shell_config.json")
    print(shell.execute_command("echo Hello from cross-platform shell"))