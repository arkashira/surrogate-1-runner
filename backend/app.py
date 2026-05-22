"""
Flask application exposing a /metrics endpoint for Prometheus scraping.
"""

from flask import Flask, Response
from prometheus_client import generate_latest, REGISTRY

app = Flask(__name__)


@app.route("/metrics")
def metrics():
    """
    Return the current Prometheus metrics.
    """
    return Response(generate_latest(REGISTRY), mimetype="text/plain; version=0.0.4")


if __name__ == "__main__":
    # Run the Flask app on port 8000 by default
    app.run(host="0.0.0.0", port=8000)