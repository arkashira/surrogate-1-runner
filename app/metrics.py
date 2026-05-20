"""Prometheus metric definitions used by the service."""
from prometheus_client import Histogram, Counter, generate_latest

# Exact bucket list required by the spec
WORKFLOW_LATENCY = Histogram(
    "surrogate_workflow_latency_seconds",
    "Workflow latency in seconds",
    ["workflow_name", "status"],
    buckets=[0.01, 0.05, 0.1, 0.5, 1, 5],
)

# Optional: a counter to show total executions (useful for alerts)
WORKFLOW_COUNT = Counter(
    "surrogate_workflow_total",
    "Total number of workflow executions",
    ["workflow_name", "status"],
)

def record_workflow(workflow_name: str, success: bool, duration: float) -> None:
    """Record a single workflow execution."""
    status = "success" if success else "failure"
    WORKFLOW_LATENCY.labels(workflow_name=workflow_name, status=status).observe(duration)
    WORKFLOW_COUNT.labels(workflow_name=workflow_name, status=status).inc()