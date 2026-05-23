import tracemalloc
import psutil
import time

class MemoryUsageAnalyzer:
    def __init__(self):
        self.tracemalloc_enabled = False

    def start_tracing(self):
        tracemalloc.start()
        self.tracemalloc_enabled = True

    def stop_tracing(self):
        if self.tracemalloc_enabled:
            current, peak = tracemalloc.get_traced_memory()
            print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
            tracemalloc.stop()
            self.tracemalloc_enabled = False

    def get_process_memory(self):
        process = psutil.Process()
        mem_info = process.memory_info()
        return mem_info.rss / 1024 / 1024  # Convert bytes to MB

    def monitor_memory(self, interval=1):
        while True:
            print(f"Memory usage: {self.get_process_memory()} MB")
            time.sleep(interval)

def analyze_memory_usage():
    analyzer = MemoryUsageAnalyzer()
    analyzer.start_tracing()
    
    # Simulate parsing operations here
    # For example, parse a large data stream
    
    time.sleep(5)  # Simulate some work
    
    analyzer.stop_tracing()

if __name__ == "__main__":
    analyze_memory_usage()