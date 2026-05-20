import os
import subprocess
import yaml
from time import sleep

class GPUDiscovery:
    def __init__(self):
        self.gpus = []
        self.bridge_config_path = '/opt/axentx/surrogate-1/firmware/bridge_config.yaml'

    def discover_gpus(self):
        try:
            lspci_output = subprocess.check_output(['lspci', '-v']).decode('utf-8')
            for line in lspci_output.split('\n'):
                if 'VGA compatible controller' in line:
                    self.gpus.append(line.strip())
            return self.gpus
        except Exception as e:
            print(f"Error discovering GPUs: {e}")
            return []

    def create_bridge_config(self):
        config = {
            'gpus': self.gpus,
            'bridge': {
                'type': 'auto',
                'load_balancing': True
            }
        }
        with open(self.bridge_config_path, 'w') as f:
            yaml.dump(config, f)

    def run(self):
        self.discover_gpus()
        self.create_bridge_config()

if __name__ == "__main__":
    gpu_discovery = GPUDiscovery()
    gpu_discovery.run()
    # Wait for 10 seconds to ensure the configuration is applied
    sleep(10)