from prometheus_client import Gauge, start_http_server
import time
import psutil

# Start up the server to expose the metrics.
start_http_server(8000)

# Create a metric to track time spent and requests made.
MEMORY_USAGE_GAUGE = Gauge('surrogate_parser_memory_bytes', 'Memory usage of the parser in bytes')

def export_memory_usage():
    while True:
        # Get current process memory usage
        process = psutil.Process()
        mem_info = process.memory_info()
        MEMORY_USAGE_GAUGE.set(mem_info.rss)
        time.sleep(5)

if __name__ == '__main__':
    export_memory_usage()