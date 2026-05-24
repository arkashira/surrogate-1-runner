import psutil
import time
from datetime import datetime

class ScalingMetricsMonitor:
    def __init__(self, interval=60):
        self.interval = interval

    def monitor_performance(self):
        while True:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_info = psutil.virtual_memory()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"{timestamp} - CPU Usage: {cpu_percent}%")
            print(f"{timestamp} - Memory Usage: {memory_info.percent}%")
            print(f"{timestamp} - Available Memory: {memory_info.available / (1024 * 1024)} MB")

            # Log or send these metrics to a monitoring system here
            
            time.sleep(self.interval)

if __name__ == "__main__":
    monitor = ScalingMetricsMonitor()
    monitor.monitor_performance()