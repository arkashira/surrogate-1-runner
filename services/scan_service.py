import json
from packaging import version   # pip install packaging

def load_current_signature(service_name: str, deployment_id: str) -> dict:
    """
    Replace this stub with the real retrieval logic (e.g., read from
    a storage bucket, call another micro‑service, etc.).
    """
    # Mocked example – in production fetch real data
    return {"version": "1.2.3", "hash": "abc123"}

def load_stored_spec(service_name: str) -> dict:
    """
    Load the previously‑approved spec for the given service.
    """
    # Mocked example – replace with DB/FS lookup
    return {"version": "1.2.0", "hash": "abc123"}

def compare_signatures(current: dict, stored: dict) -> dict:
    """
    Returns a dict:
        {
            "differences": [...],
            "breaking": bool
        }
    """
    diffs = []
    breaking = False

    if current["hash"] != stored["hash"]:
        diffs.append("hash mismatch")
        breaking = True

    if current["version"] != stored["version"]:
        diffs.append(
            f"version changed from {stored['version']} to {current['version']}"
        )
        # Major version bump is breaking
        if version.parse(current["version"]).release[0] != version.parse(stored["version"]).release[0]:
            breaking = True

    return {"differences": diffs, "breaking": breaking}

def run_signature_scan(service_name: str, deployment_id: str) -> dict:
    """
    Orchestrates the whole scan and returns a serialisable result.
    """
    current = load_current_signature(service_name, deployment_id)
    stored = load_stored_spec(service_name)

    comparison = compare_signatures(current, stored)

    return {
        "service": service_name,
        "deployment_id": deployment_id,
        **comparison,
        "status": "completed"
    }