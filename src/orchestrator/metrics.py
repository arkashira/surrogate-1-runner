from prometheus_client import (
    Histogram,
    Counter,
    CollectorRegistry,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

# ----------------------------------------------------------------------
# Registry – isolated from the global default (helps testing & avoids
# accidental metric duplication when the module is re‑loaded).
# ----------------------------------------------------------------------
registry = CollectorRegistry()

# ----------------------------------------------------------------------
# Metrics
# ----------------------------------------------------------------------
WORKFLOW_LATENCY = Histogram(
    name="surrogate_workflow_latency_seconds",
    documentation="Latency of surrogate workflows in seconds",
    labelnames=["workflow_name", "status"],
    buckets=[0.01, 0.05, 0.1, 0.5, 1, 5],
    registry=registry,
)

WORKFLOW_COUNT = Counter(
    name="surrogate_workflow_executions_total",
    documentation="Total number of workflow executions",
    labelnames=["workflow_name", "status"],
    registry=registry,
)

# ----------------------------------------------------------------------
# Public helper – record both latency and count in one call
# ----------------------------------------------------------------------
def record_workflow_metrics(workflow_name: str, duration: float, status: str) -> None:
    """
    Record the duration and status of a workflow execution.

    Parameters
    ----------
    workflow_name: str
        Logical name of the workflow (e.g. "dataset_ingest").
    duration: float
        Execution time in seconds.
    status: str
        Either "success" or "failure".
    """
    WORKFLOW_LATENCY.labels(workflow_name=workflow_name, status=status).observe(duration)
    WORKFLOW_COUNT.labels(workflow_name=workflow_name, status=status).inc()


# ----------------------------------------------------------------------
# HTTP endpoint – serves the metrics from the custom registry
# ----------------------------------------------------------------------
def _run_metrics_http_server(port: int = 8000) -> None:
    """Blocking call that runs a tiny WSGI server exposing /metrics."""
    from wsgiref.simple_server import make_server, WSGIRequestHandler

    class _SilentHandler(WSGIRequestHandler):
        # Silence the default request logging (keeps container logs clean)
        def log_message(self, format, *args):
            pass

    def app(environ, start_response):
        if environ.get("PATH_INFO") == "/metrics":
            data = generate_latest(registry)
            start_response("200 OK", [("Content-Type", CONTENT_TYPE_LATEST)])
            return [data]
        start_response("404 Not Found", [("Content-Type", "text/plain")])
        return [b"Not Found"]

    httpd = make_server("", port, app, handler_class=_SilentHandler)
    httpd.serve_forever()


def start_metrics_server(port: int = 8000) -> None:
    """
    Launch the metrics HTTP server in a daemon thread.
    Call this once at process start‑up.
    """
    import threading

    thread = threading.Thread(target=_run_metrics_http_server, args=(port,), daemon=True)
    thread.start()