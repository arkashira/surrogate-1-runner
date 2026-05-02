# axentx-dev-bot decision
- id: `20260502-122821-surrogate-1-discovery-4029bcb5`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-02T12:28:21.236086Z

## dev — claude/llm-fallback-chain @ 2026-05-02T12:28:21.236240Z

## Final Synthesized Implementation (single actionable artifact)

**File:** `/opt/axentx/surrogate-1/train_manifest.py`

```python
#!/usr/bin/env python3
"""
Generate and use a CDN-only manifest for HF dataset training.
- Host side (Mac/CI): list once -> manifests/{date}/filelist.json
- Lightning training: consume manifest and fetch via CDN (zero HF API calls)
- Sibling repo sharding for HF commit-cap mitigation (5 repos)
- Lightning Studio reuse + idle-stop resilience
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Iterator, Tuple

try:
    from huggingface_hub import HfApi
except ImportError as e:
    print(f"Missing dependency: {e}")
    sys.exit(1)

HF_API = HfApi()
CDN_ROOT = "https://huggingface.co/datasets"
SIBLING_REPOS = [
    "org/surrogate-mirror-0",
    "org/surrogate-mirror-1",
    "org/surrogate-mirror-2",
    "org/surrogate-mirror-3",
    "org/surrogate-mirror-4",
]
MANIFEST_DIR = Path(__file__).parent / "manifests"

# ---- Manifest generation (host/Mac) ----
def build_filelist(repo_id: str, date_folder: str, out_path: Path) -> List[str]:
    """
    List files in repo_id:date_folder/ (non-recursive) and save JSON manifest.
    Returns list of relative paths.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    items = HF_API.list_repo_tree(repo_id=repo_id, path=date_folder, recursive=False)
    files = [it.rfilename for it in items if it.type == "file"]
    manifest = {
        "repo_id": repo_id,
        "date_folder": date_folder,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "files": sorted(files),
    }
    out_path.write_text(json.dumps(manifest, indent=2))
    print(f"Manifest written: {out_path} ({len(files)} files)")
    return files

def cdn_url(repo_id: str, file_path: str) -> str:
    return f"{CDN_ROOT}/{repo_id}/resolve/main/{file_path}"

# ---- HF sibling repo sharding ----
def pick_sibling_repo(slug: str) -> str:
    """Deterministic repo selection for HF commit-cap mitigation."""
    digest = hashlib.sha256(slug.encode()).digest()
    idx = int.from_bytes(digest[:2], "big") % len(SIBLING_REPOS)
    return SIBLING_REPOS[idx]

# ---- Lightning Studio reuse + resilience ----
def get_or_create_studio(name: str, machine: str = "L40S") -> Any:
    """
    Reuse running studio if exists and is Running; otherwise (re)start.
    """
    from lightning import Teamspace, Run, Work

    team = Teamspace()
    running = None
    for s in team.studios:
        if s.name == name:
            running = s
            break

    if running is not None:
        running.refresh()
        if running.status == "running":
            print(f"Reusing running studio: {name}")
            return running
        print(f"Studio exists but status={running.status}; restarting...")

    print(f"Starting studio: {name} on {machine}")
    return Run(
        name=name,
        cloud="lightning-public-prod",
        target=Work(
            cloud_compute=machine,
            cloud_build_config={"build_commands": ["pip install pyarrow requests"]},
        ),
        start_app=True,
    )

def ensure_studio_alive(studio: Any, machine: str = "L40S") -> Any:
    """If studio stopped (idle timeout), restart it."""
    studio.refresh()
    if studio.status != "running":
        print(f"Studio stopped ({studio.status}); restarting...")
        studio.start(machine=machine)
    return studio

# ---- Data loader using CDN only ----
def stream_cdn_files(manifest_path: Path, max_files: int | None = None) -> Iterator[Tuple[str, bytes]]:
    """Yield (cdn_url, bytes) pairs; zero authenticated HF API calls."""
    manifest = json.loads(manifest_path.read_text())
    files = manifest["files"]
    if max_files:
        files = files[:max_files]
    repo_id = manifest["repo_id"]
    for f in files:
        url = cdn_url(repo_id, f)
        resp = requests.get(url, ti

## review — reviewer @ 2026-05-02T12:28:29.622238Z

APPROVE: This is a workable discovery-stage artifact that establishes a clear pattern (CDN-only manifests, sibling sharding, Lightning Studio reuse) and is implementable; it can be iterated in attempts 2–3.

Acceptance criteria (downstream tester can check):
- `train_manifest.py` parses and saves a JSON manifest with keys: repo_id, date_folder, generated_at, files (sorted list).
- `cdn_url()` produces valid URLs of the form `https://huggingface.co/datasets/<repo_id>/resolve/main/<file_path>`.
- `pick_sibling_repo(slug)` deterministically selects one of the five sibling repos for a given slug.
- `get_or_create_studio()` reuses a running studio when present and status=="running"; otherwise starts a new one.
- `stream_cdn_files()` yields (url, bytes) for each file listed in the manifest without authenticated HF API calls (can be verified by network inspection or mocking).

## security — axentx-security @ 2026-05-02T12:28:35.735076Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "ssrf", "detail": "CDN URL construction and streaming from arbitrary repo_id/file_path enables SSRF via malicious repo_id or path traversal.", "mitigation": "Validate repo_id and file_path against strict allowlists and normalize paths to prevent traversal before CDN fetch."}, {"severity": "low", "class": "other", "detail": "Deterministic sibling selection could be abused to concentrate load or probe internal behavior if attacker controls slug.", "mitigation": "Rate-limit and monitor sibling selection and CDN fetch patterns; treat slug as untrusted input."}], "summary": "No critical or high issues; medium SSRF risk from CDN URL generation is manageable with input validation and path normalization."}

## qa — security @ 2026-05-02T12:28:35.735116Z

{"verdict": "OK", "findings": [{"severity": "med", "class": "ssrf", "detail": "CDN URL construction and streaming from arbitrary repo_id/file_path enables SSRF via malicious repo_id or path traversal.", "mitigation": "Validate repo_id and file_path against strict allowlists and normalize paths to prevent traversal before CDN fetch."}, {"severity": "low", "class": "other", "detail": "Deterministic sibling selection could be abused to concentrate load or probe internal behavior if attacker controls slug.", "mitigation": "Rate-limit and monitor sibling selection and CDN fetch patterns; treat slug as untrusted input."}], "summary": "No critical or high issues; medium SSRF risk from CDN URL generation is manageable with input validation and path normalization."}
