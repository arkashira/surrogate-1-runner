import random
import datetime
from typing import List, Dict

from flask import Flask, render_template, jsonify, request

app = Flask(__name__, template_folder="templates")


# ---------- Mock data generation ----------
_RESOURCE_TYPES = ["EC2", "S3", "RDS", "Lambda", "EKS"]
_LOCATIONS = ["us-east-1", "us-west-2", "eu-central-1", "ap-southeast-2"]


def _generate_cost_entry() -> Dict:
    """Create a single cost entry with realistic‑looking values."""
    return {
        "resource_type": random.choice(_RESOURCE_TYPES),
        "location": random.choice(_LOCATIONS),
        "cost": round(random.uniform(0.01, 150.00), 2),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }


def get_cost_data(limit: int = 50) -> List[Dict]:
    """
    Return a list of recent cost entries.
    In a real implementation this would query a time‑series store or
    cloud provider billing API.
    """
    return [_generate_cost_entry() for _ in range(limit)]


# ---------- Routes ----------
@app.route("/")
def index():
    """Render the dashboard UI."""
    return render_template("index.html", resource_types=_RESOURCE_TYPES, locations=_LOCATIONS)


@app.route("/api/costs")
def api_costs():
    """
    Return JSON cost data, optionally filtered by ``resource_type`` and ``location``.
    Query parameters:
        resource_type – one of the known types or omitted for all
        location      – one of the known locations or omitted for all
    """
    resource_type = request.args.get("resource_type")
    location = request.args.get("location")

    data = get_cost_data()

    if resource_type:
        data = [d for d in data if d["resource_type"] == resource_type]
    if location:
        data = [d for d in data if d["location"] == location]

    return jsonify(data)


# ---------- Entry point ----------
if __name__ == "__main__":
    # Enable debug mode for rapid iteration; in production run via a WSGI server.
    app.run(host="0.0.0.0", port=5000, debug=True)