from prometheus_client import Gauge, start_http_server
import psutil
import time

# Create a gauge metric for memory usage
memory_usage = Gauge('surrogate_parser_memory_bytes', 'Memory usage of the parser in bytes')

def update_metrics():
    while True:
        # Get the current process memory usage
        process = psutil.Process()
        mem_info = process.memory_info()
        memory_usage.set(mem_info.rss)

        # Sleep for 5 seconds
        time.sleep(5)

# Start the Prometheus HTTP server on port 8000
start_http_server(8000)
update_metrics()