import psutil
import time
from typing import Dict, List
import logging

class MemoryMonitor:
    def __init__(self, interval: float = 1.0):
        self.interval = interval
        self.process = psutil.Process()
        self.logger = logging.getLogger(__name__)

    def get_memory_usage(self) -> Dict[str, float]:
        """Get current memory usage statistics."""
        memory_info = self.process.memory_info()
        return {
            'rss': memory_info.rss / (1024 ** 2),  # in MB
            'vms': memory_info.vms / (1024 ** 2),  # in MB
            'percent': self.process.memory_percent()
        }

    def monitor(self, duration: float) -> List[Dict[str, float]]:
        """Monitor memory usage for a specified duration."""
        memory_samples = []
        end_time = time.time() + duration

        while time.time() < end_time:
            memory_usage = self.get_memory_usage()
            memory_samples.append(memory_usage)
            time.sleep(self.interval)

        return memory_samples

    def log_memory_usage(self, duration: float):
        """Log memory usage over a specified duration."""
        memory_samples = self.monitor(duration)
        for sample in memory_samples:
            self.logger.info(
                f"Memory Usage - RSS: {sample['rss']:.2f} MB, "
                f"VMS: {sample['vms']:.2f} MB, "
                f"Percent: {sample['percent']:.2f}%"
            )

if __name__ == "__main__":
    monitor = MemoryMonitor(interval=1.0)
    monitor.log_memory_usage(duration=60.0)  # Monitor for 60 seconds