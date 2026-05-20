from prometheus_client import start_http_server, Histogram, Counter

class IngestionMetrics:
    def __init__(self):
        self.ingestion_duration_seconds = Histogram('ingestion_duration_seconds', 'Duration of data ingestion process')
        self.ingestion_failures_total = Counter('ingestion_failures_total', 'Total number of ingestion failures')

    def observe_duration(self, duration):
        self.ingestion_duration_seconds.observe(duration)

    def increment_failure(self):
        self.ingestion_failures_total.inc()

def initialize_metrics():
    start_http_server(8000)
    return IngestionMetrics()