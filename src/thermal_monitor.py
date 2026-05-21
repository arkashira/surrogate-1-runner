import time
import subprocess
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThermalMonitor:
    def __init__(self):
        self.gpu_count = self._get_gpu_count()
        self.fan_speeds = [50] * self.gpu_count  # Default fan speed

    def _get_gpu_count(self) -> int:
        try:
            result = subprocess.run(['nvidia-smi', '-L'], capture_output=True, text=True)
            if result.returncode == 0:
                return len(result.stdout.split('\n')) - 1
            else:
                logger.error("Failed to get GPU count")
                return 0
        except Exception as e:
            logger.error(f"Error getting GPU count: {e}")
            return 0

    def get_gpu_temps(self) -> List[float]:
        temps = []
        try:
            result = subprocess.run(['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'], capture_output=True, text=True)
            if result.returncode == 0:
                temps = [float(temp.strip()) for temp in result.stdout.split('\n') if temp.strip()]
        except Exception as e:
            logger.error(f"Error getting GPU temps: {e}")
        return temps

    def adjust_fan_speeds(self, temps: List[float]) -> None:
        for i, temp in enumerate(temps):
            if temp > 85:
                self.fan_speeds[i] = min(100, self.fan_speeds[i] + 10)
                logger.warning(f"GPU {i} temperature is {temp}°C. Increasing fan speed to {self.fan_speeds[i]}%")
            elif temp < 75:
                self.fan_speeds[i] = max(30, self.fan_speeds[i] - 5)
                logger.info(f"GPU {i} temperature is {temp}°C. Decreasing fan speed to {self.fan_speeds[i]}%")

    def monitor(self) -> None:
        while True:
            temps = self.get_gpu_temps()
            if temps:
                self.adjust_fan_speeds(temps)
            time.sleep(5)  # Monitor every 5 seconds

if __name__ == "__main__":
    monitor = ThermalMonitor()
    monitor.monitor()