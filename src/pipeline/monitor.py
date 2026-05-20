import time
import logging
from typing import Dict, Any

class PerformanceMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.metrics = {}

    def start_timer(self, process_name: str) -> None:
        self.metrics[process_name] = {'start_time': time.time()}

    def end_timer(self, process_name: str) -> None:
        if process_name in self.metrics:
            self.metrics[process_name]['end_time'] = time.time()
            self.metrics[process_name]['duration'] = self.metrics[process_name]['end_time'] - self.metrics[process_name]['start_time']
            self.log_metrics(process_name)

    def log_metrics(self, process_name: str) -> None:
        if process_name in self.metrics:
            duration = self.metrics[process_name]['duration']
            self.logger.info(f"Performance metrics for {process_name}: Duration = {duration} seconds")

    def get_metrics(self) -> Dict[str, Any]:
        return self.metrics