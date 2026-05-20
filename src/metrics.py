from prometheus_client import Counter, Histogram

# Create a histogram to track ingestion duration
INGESTION_DURATION = Histogram(
    'ingestion_duration_seconds',
    'Time spent processing ingestion',
    buckets=[0.1, 0.5, 1, 2.5, 5, 10, 15, 20, 30, 60, 120, 180, 300, 600]
)

# Create a counter to track ingestion failures
INGESTION_FAILURES = Counter(
    'ingestion_failures_total',
    'Total number of ingestion failures'
)