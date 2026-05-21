import os
import socket
import time
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

class MetricsCollector:
    def __init__(self):
        # Initialize MeterProvider and set it as the global meter provider
        self.meter_provider = MeterProvider()
        metrics.set_meter_provider(self.meter_provider)
        
        # Get the Meter instance for our application
        self.meter = metrics.get_meter(__name__)
        
        # Create a Gauge metric to track the number of open file descriptors
        self.open_fd_gauge = self.meter.create_gauge(
            name="fd.scout.open_total",
            description="Number of open file descriptors",
            unit="1"
        )
        
        # Retrieve container ID and hostname
        self.container_id = os.getenv("CONTAINER_ID", "unknown")
        self.hostname = socket.gethostname()
        
        # Set the interval for metric collection
        self.interval = int(os.getenv("METRIC_INTERVAL", 30))
        
        # Initialize the OTLP exporter and metric reader
        exporter = OTLPMetricExporter(endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"))
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=self.interval * 1000)
        self.meter_provider.add_metric_reader(reader)

    def collect_open_fd(self):
        try:
            # Count the number of open file descriptors
            with open("/proc/self/fd", "r") as fd:
                open_fds = len(fd.readlines())
            
            # Record the metric with appropriate labels
            self.open_fd_gauge.record(
                open_fds,
                {"container_id": self.container_id, "hostname": self.hostname}
            )
        except Exception as e:
            print(f"Error collecting open file descriptors: {e}")

    def start(self):
        # Start the metric collection loop
        while True:
            self.collect_open_fd()
            time.sleep(self.interval)

# Example usage:
if __name__ == "__main__":
    collector = MetricsCollector()
    collector.start()