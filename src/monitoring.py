import time
import threading
import psutil
from prometheus_client import start_http_server, Gauge
from .config import AppConfig

class PerformanceMonitor:
    def __init__(self, config: AppConfig):
        self.config = config
        self.cpu = Gauge('cpu_usage_percent', 'CPU usage percentage')
        self.memory = Gauge('memory_usage_percent', 'Memory usage percentage')
        self.disk = Gauge('disk_usage_percent', 'Disk usage percentage')
        self.network = Gauge('network_io_bytes', 'Network I/O bytes')
        self._stop_event = threading.Event()

    def _collect_once(self):
        """Collect a single sample – used by tests."""
        self.cpu.set(psutil.cpu_percent(interval=None))
        self.memory.set(psutil.virtual_memory().percent)
        self.disk.set(psutil.disk_usage('/').percent)
        net = psutil.net_io_counters()
        self.network.set(net.bytes_sent + net.bytes_recv)

    def _run(self):
        """Background thread that samples every 15 s."""
        while not self._stop_event.is_set():
            self._collect_once()
            # Sleep *after* collecting so we get a sample immediately on start.
            self._stop_event.wait(15)

    def start(self):
        """Start the HTTP server and the background collector."""
        start_http_server(self.config.metrics_port)
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        """Gracefully stop the collector thread."""
        self._stop_event.set()
        self._thread.join()