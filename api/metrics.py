from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import threading

# Global lock for thread-safe metric updates
_metrics_lock = threading.Lock()

# Request duration histogram (in seconds)
_request_duration = Histogram(
    name='costradar_request_duration_seconds',
    documentation='Request latency in seconds',
    labelnames=['endpoint'],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)
)

# Error counter
_errors_total = Counter(
    name='costradar_errors_total',
    documentation='Total number of errors by endpoint',
    labelnames=['endpoint', 'status_code']
)

# Health check counter
_health_checks_total = Counter(
    name='costradar_health_checks_total',
    documentation='Total health checks performed',
    labelnames=['status']
)

def get_metrics():
    """Return Prometheus metrics as bytes."""
    return generate_latest()

def record_request_duration(endpoint, duration_seconds):
    """Record request duration for an endpoint."""
    with _metrics_lock:
        _request_duration.labels(endpoint=endpoint).observe(duration_seconds)

def record_error(endpoint, status_code):
    """Record an error for an endpoint."""
    with _metrics_lock:
        _errors_total.labels(endpoint=endpoint, status_code=str(status_code)).inc()

def record_health_check(status):
    """Record a health check."""
    with _metrics_lock:
        _health_checks_total.labels(status=status).inc()