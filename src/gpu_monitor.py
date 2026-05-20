import subprocess

class GPUMonitor:
    def __init__(self):
        self.gpu_id = 0

    def get_power_consumption(self):
        result = subprocess.run(['nvidia-smi', '--query-gpu=power.draw', '--format=csv,noheader,nounits', f'--id={self.gpu_id}'], capture_output=True, text=True)
        return float(result.stdout.strip())

    def get_temperature(self):
        result = subprocess.run(['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits', f'--id={self.gpu_id}'], capture_output=True, text=True)
        return float(result.stdout.strip())

    def reduce_power_consumption(self):
        subprocess.run(['nvidia-smi', '-pl', '150', f'-i {self.gpu_id}'])

    def increase_power_consumption(self):
        subprocess.run(['nvidia-smi', '-pl', '250', f'-i {self.gpu_id}'])