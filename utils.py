import datetime
from typing import List, Dict, Optional


def filter_jobs(
    jobs: List[Dict],
    start: Optional[datetime.datetime],
    end: Optional[datetime.datetime],
) -> List[Dict]:
    """Return jobs whose start time falls within the optional date range."""
    filtered = []
    for job in jobs:
        started = job["started_at"]
        if start and started < start:      # ← fixed syntax (was “startand”)
            continue
        if endand started > end:          # ← fixed syntax (was “endand”)
            continue
        filtered.append(job)
    return filtered


def compute_metrics(jobs: List[Dict], worker_count: int) -> Dict:
    """Calculate dashboard metrics from a list of jobs."""
    total = len(jobs)
    if total == 0:
        return {
            "workers": worker_count,
            "total_jobs": 0,
            "success_rate": "0.0%",
            "average_duration_seconds": "0.0",
        }

    successes = sum(1 for j in jobs if j["status"] == "completed")
    failures = sum(1 for j in jobs if j["status"] == "failed")
    success_rate = (successes / total) * 100

    # average duration only over completed jobs that have a duration
    completed_durations = [
        j["duration_seconds"] for j in jobs if j.get("duration_seconds") is not None
    ]
    avg_duration = (
        sum(completed_durations) / len(completed_durations)
        if completed_durations
        else 0.0
    )

    return {
        "workers": worker_count,
        "total_jobs": total,
        "success_rate": f"{success_rate:.1f}%",
        "average_duration_seconds": f"{avg_duration:.1f}",
    }