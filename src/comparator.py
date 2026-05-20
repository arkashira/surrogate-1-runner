import json
from typing import Dict, Tuple, List
from .model import Signature

def _diff_sets(current: set, baseline: set, label: str) -> List[str]:
    added   = current - baseline
    removed = baseline - current
    msgs = []
    if added:
        msgs.append(f"{label} added: {sorted(added)}")
    if removed:
        msgs.append(f"{label} removed: {sorted(removed)}")
    return msgs

def compare_signature(current: Signature, baseline: Signature) -> Tuple[bool, str]:
    """
    Returns ``(drift_detected, human_readable_diff)``.
    A drift is flagged when *any* of method, path or header set differs.
    The diff format mirrors the Go implementation for familiarity:
        method: "GET" → "POST"
        path:   "/old" → "/new"
        header "Accept": "application/json" → "text/plain"
        header "X-Extra": missing in current (baseline "foo")
        header "X-Auth": added in current (value "bar")
    """
    diffs: List[str] = []

    # 1️⃣ method
    if current.method.strip().upper() != baseline.method.strip().upper():
        diffs.append(f'method: "{baseline.method}" → "{current.method}"')

    # 2️⃣ path
    if current.path.strip() != baseline.path.strip():
        diffs.append(f'path: "{baseline.path}" → "{current.path}"')

    # 3️⃣ headers – detect missing, extra or changed values
    checked = set()
    for k, v_baseline in baseline.headers.items():
        if k in current.headers:
            v_current = current.headers[k]
            if v_current != v_baseline:
                diffs.append(f'header "{k}": "{v_baseline}" → "{v_current}"')
        else:
            diffs.append(f'header "{k}": missing in current (baseline "{v_baseline}")')
        checked.add(k)

    for k, v_current in current.headers.items():
        if k not in checked:
            diffs.append(f'header "{k}": added in current (value "{v_current}")')

    # Optional set‑diff summary (useful for bulk path‑level comparison)
    # drifts = _diff_sets(set(current.headers), set(baseline.headers), "header")

    drift = bool(diffs)
    diff_str = "\n".join(diffs) if drift else ""
    return drift, diff_str