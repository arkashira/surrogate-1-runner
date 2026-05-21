import subprocess
import re
from typing import List, Dict

class GPUDiscovery:
    def __init__(self):
        self.gpu_info = []

    def detect_gpus(self) -> List[Dict]:
        """Detect and return information about compatible GPUs."""
        try:
            # Run lspci command to get GPU information
            result = subprocess.run(['lspci', '-nnk'], capture_output=True, text=True)
            output = result.stdout

            # Use regex to find GPU information
            gpu_pattern = re.compile(r'VGA compatible controller.*?\n.*?Kernel driver in use: (.*?)\n.*?Kernel modules: (.*?)\n', re.DOTALL)
            gpu_matches = gpu_pattern.findall(output)

            for match in gpu_matches:
                driver, modules = match
                self.gpu_info.append({
                    'driver': driver.strip(),
                    'modules': modules.strip()
                })

            return self.gpu_info
        except Exception as e:
            print(f"Error detecting GPUs: {e}")
            return []

    def generate_load_balancing_profile(self) -> Dict:
        """Generate an optimal load-balancing profile for the detected GPUs."""
        if not self.gpu_info:
            self.detect_gpus()

        # Simple load-balancing profile based on the number of GPUs
        num_gpus = len(self.gpu_info)
        if num_gpus == 0:
            return {}

        profile = {
            'gpu_count': num_gpus,
            'load_balancing': 'round_robin',
            'performance_overlay': True
        }

        return profile