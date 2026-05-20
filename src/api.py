"""
Flask API for surrogate-1 service.
Exposes Prometheus metrics with bearer token authentication.
"""

import os
import yaml
from flask import Flask, request, Response, abort
from prometheus_client import (
    CollectorRegistry,
    Counter,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

METRICS_CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), 
    "metrics.yaml"
)

def load_metrics_config(path: str) -> dict:
    """Load metrics configuration from YAML file."""
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        print(f"Warning: Config file not found at {path}")
        return {}
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return {}

# Load token from metrics.yaml
metrics_cfg = load_metrics_config(METRICS_CONFIG_PATH)
METRICS_BEARER_TOKEN = metrics_cfg.get("bearer_token", "")

if not METRICS_BEARER_TOKEN:
    print("WARNING: No bearer_token configured in metrics.yaml")

# --------------------------------------------------------------------------- #
# Prometheus metrics (custom registry to avoid double registration)
# --------------------------------------------------------------------------- #

registry = CollectorRegistry()

surrogate_checks_total = Counter(
    "surrogate_checks_total",
    "Total number of surrogate checks performed",
    ["service"],
    registry=registry,
)

surrogate_checks_failed = Counter(
    "surrogate_checks_failed",
    "Total number of surrogate checks that failed",
    ["service"],
    registry=registry,
)

# --------------------------------------------------------------------------- #
# Flask application
# --------------------------------------------------------------------------- #

app = Flask(__name__)

def require_bearer_token(f):
    """Decorator to enforce bearer token authentication."""
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        
        if not auth_header:
            abort(401, description="Missing Authorization header")
        
        if not auth_header.startswith("Bearer "):
            abort(401, description="Invalid Authorization format")
        
        token = auth_header.split(" ", 1)[1]
        
        if token != METRICS_BEARER_TOKEN:
            abort(403, description="Invalid bearer token")
        
        return f(*args, **kwargs)
    
    wrapper.__name__ = f.__name__
    return wrapper

@app.route("/metrics")
@require_bearer_token
def metrics():
    """
    Expose Prometheus metrics.
    
    Returns metrics with correct Content-Type for Prometheus scraping.
    """
    return Response(
        generate_latest(registry),
        mimetype=CONTENT_TYPE_LATEST,
    )

# --------------------------------------------------------------------------- #
# Counter increment functions (call these from your application)
# --------------------------------------------------------------------------- #

def increment_check_total(service_name: str):
    """Increment the total checks counter for a service."""
    surrogate_checks_total.labels(service=service_name).inc()

def increment_check_failed(service_name: str):
    """Increment the failed checks counter for a service."""
    surrogate_checks_failed.labels(service=service_name).inc()

# --------------------------------------------------------------------------- #
# Testing / development
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Initialize counters with sample data for testing
    surrogate_checks_total.labels(service="surrogate-1").inc(10)
    surrogate_checks_failed.labels(service="surrogate-1").inc(2)
    
    app.run(host="0.0.0.0", port=5000, debug=True)