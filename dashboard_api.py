import datetime
from flask import Blueprint, jsonify, request, abort
from models import _jobs, WORKER_COUNT
from utils import filter_jobs, compute_metrics

dashboard_api = Blueprint("dashboard_api", __name__)


def _parse_datetime(param: str) -> datetime.datetime:
    """Parse an ISO‑8601 string (with optional Z suffix) into a naive UTC datetime."""
    if not param:
        return None
    # Replace Z with +00:00 to make it timezone‑aware, then strip timezone info
    # (we keep naive datetimes to match the in‑memory store)
    iso = param.replace("Z", "+00:00")
    try:
        dt = datetime.datetime.fromisoformat(iso)
        return dt.replace(tzinfo=None)  # drop tz → naive UTC
    except ValueError:
        abort(400, description="Invalid datetime format. Use ISO‑8601 (e.g., 2024-05-01T00:00:00Z).")


@dashboard_api.route("/api/dashboard", methods=["GET"])
def dashboard():
    """Return metrics + job list, optionally filtered by start/end."""
    start_str = request.args.get("start")
    end_str = request.args.get("end")

    start_dt = _parse_datetime(start_str)
    end_dt = _parse_datetime(end_str)

    # Filter
    filtered = filter_jobs(_jobs, start_dt, end_dt)

    # Metrics
    metrics = compute_metrics(filtered, WORKER_COUNT)

    # Serialize jobs for JSON (naive ISO strings)
    jobs_serialized = []
    for job in filtered:
        jobs_serialized.append({
            "id": job["id"],
            "status": job["status"],
            "started_at": job["started_at"].isoformat() + "Z",
            "ended_at": job["ended_at"].isoformat() + "Z" if job["ended_at"] else None,
            "duration_seconds": job["duration_seconds"],
        })

    return jsonify({
        "metrics": metrics,
        "jobs": jobs_serialized,
    })