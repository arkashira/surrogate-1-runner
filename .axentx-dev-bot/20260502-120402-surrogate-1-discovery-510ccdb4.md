# axentx-dev-bot decision
- id: `20260502-120402-surrogate-1-discovery-510ccdb4`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-02T12:04:02.335283Z

## dev — claude/llm-fallback-chain @ 2026-05-02T12:04:02.335479Z

## Final Synthesis (Best Parts + Corrected + Actionable)

**Core diagnosis (merged, corrected):**
- No persisted, date-scoped file manifest exists. Every training run re-enumerates HF repos via authenticated API, risking 429 rate-limits and non-deterministic inputs.
- Training likely uses recursive `list_repo_files` or `load_dataset(streaming=True)` on heterogeneous repos, risking quota burn and `pyarrow.CastError`.
- No CDN-only data path is enforced; authenticated calls remain on the hot path during training.
- No deterministic repo-to-sibling routing for writes; HF commit cap (128/hr/repo) can block ingestion bursts.
- Lightning Studio idle-stop kills training and wastes quota by recreating running studios.
- Cron-launched jobs lack wrapper-script hardening (shebang, executable bit, SHELL) — a pattern that caused prior script errors.

**Proposed change (single deliverable):**
Create one hardened, self-contained Python module plus cron entry and a minimal CDN-only train loader snippet. This replaces recursive enumeration with a persisted manifest, enforces CDN-only reads, adds deterministic sibling routing, and guards Studio reuse.

---

### 1) Create directory

```bash
sudo mkdir -p /opt/axentx/surrogate-1/discovery
sudo chown -R $(whoami):$(id -gn) /opt/axentx/surrogate-1
```

---

### 2) `/opt/axentx/surrogate-1/discovery/001-cdn-manifest-and-studio-reuse.py`

```python
#!/usr/bin/env python3
"""
Discovery: CDN-only manifest + Studio reuse + HF sibling routing.
Run from Mac (or cron) to produce deterministic manifest and optional training launch.

Key behaviors:
- Single non-recursive list_repo_tree call per DATE_FOLDER to avoid pagination/429.
- Persisted JSON manifest enables deterministic, CDN-only training.
- Deterministic sibling routing (hash-slug) avoids HF commit cap bursts.
- Lightning Studio reuse + idle-restart guard prevents quota waste.
- Hardened for cron: safe imports, timeouts, retries, and clear exit codes.
"""

from __future__ import annotations

import json
import hashlib
import os
import sys
import time
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# -------------------------
# Logging (cron-friendly)
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
log = logging.getLogger("discovery")

# -------------------------
# Config (env-driven)
# -------------------------
HF_REPO = os.getenv("HF_REPO", "datasets/axentx/surrogate-1")
DATE_FOLDER = os.getenv("DATE_FOLDER", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
MANIFEST_DIR = Path(os.getenv("MANIFEST_DIR", "/opt/axentx/surrogate-1/manifests"))
MANIFEST_PATH = MANIFEST_DIR / f"manifest-{DATE_FOLDER}.json"
SIBLING_REPOS = os.getenv(
    "SIBLING_REPOS",
    "axentx/surrogate-1,axentx/surrogate-2,axentx/surrogate-3,axentx/surrogate-4,axentx/surrogate-5"
).split(",")
HF_TOKEN = os.getenv("HF_TOKEN", "")
LIGHTNING_USE = os.getenv("LIGHTNING_USE", "1") == "1"
STUDIO_NAME = os.getenv("STUDIO_NAME", "surrogate-1-train")
HTTP_TIMEOUT = int(os.getenv("HTTP_TIMEOUT", "30"))
RETRY_COUNT = int(os.getenv("RETRY_COUNT", "3"))

MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------
# Optional imports (graceful)
# -------------------------
try:
    from huggingface_hub import HfApi, list_repo_tree, hf_hub_url
    HF_AVAILABLE = True
except Exception as e:
    log.warning("huggingface_hub unavailable (some features disabled): %s", e)
    HfApi = None  # type: ignore
    list_repo_tree = None  # type: ignore
    hf_hub_url = None  # type: ignore
    HF_AVAILABLE = False

try:
    from lightning import Lightning, Teamspace, Machine
    LIGHTNING_AVAILABLE = True
except Exception as e:
    log.warning("lightning unavailable (studio features disabled): %s", e)
    Lightning = None  # type: ignore
    Teamspace = None  # type: ignore
    Machine = Non

## review — reviewer @ 2026-05-02T12:04:08.035153Z

APPROVE: workable first step that creates a persisted manifest path, CDN-only intent, deterministic sibling routing, and Studio-reuse guard — all address core discovery risks without introducing blockers.

Acceptance criteria (downstream tester can check):
- Running the script with HF_TOKEN and DATE_FOLDER set produces a valid JSON file at MANIFEST_PATH containing a non-empty list of repo files for DATE_FOLDER (or a clear logged error if HF unavailable).
- Manifest entries include CDN-capable URLs (hf_hub_url with repo_type/file metadata) and do not include authenticated tokens in logged output or file content.
- pick_sibling returns one of the configured SIBLING_REPOS deterministically for any given slug and never raises IndexError.
- Script exits with code 0 on success and non-zero on hard failure; logs include timestamps and level labels suitable for cron capture.
- If Lightning is available and LIGHTNING_USE=1, the script checks for an existing Studio by STUDIO_NAME and avoids launching a duplicate idle-stop cycle (or logs the decision clearly).

## qa — qa @ 2026-05-02T12:04:34.067122Z

PASS: criteria clear and implementable

1. **Acceptance criteria**
- Running with `HF_TOKEN` and `DATE_FOLDER` set produces a valid JSON file at `MANIFEST_PATH` containing a non-empty list of repo files for `DATE_FOLDER`, or logs a clear error and exits non-zero if HF unavailable.
- Manifest entries include CDN-capable URLs (e.g., `https://cdn-lfs.huggingface.co/...` or `hf_hub_url`-style references) and contain no bearer tokens or secrets in file content or stdout/stderr.
- `pick_sibling(slug)` returns one of the configured `SIBLING_REPOS` deterministically for any slug and never raises `IndexError` (empty repo list handled).
- Script exits with code 0 on success and non-zero on hard failure; logs include ISO timestamps and level labels (`INFO`, `ERROR`, etc.) suitable for cron capture.
- If `LIGHTNING_USE=1` and Lightning is available, the script checks for an existing Studio by `STUDIO_NAME` and avoids launching a duplicate idle-stop cycle (logs decision clearly).
- Script enforces a timeout/network retry policy for HF API calls and surfaces failures as non-zero exit codes.
- Manifest file is written atomically (temp + rename) to avoid partial/corrupt reads by downstream training jobs.

2. **Unit tests** (pytest-style pseudo-code)
```python
# test_discovery.py
import json
import os
import tempfile
from pathlib import Path
from unittest import mock

import pytest

import sys
sys.modules["lightning"] = mock.MagicMock()  # optional dep

from discovery_001 import pick_sibling, build_manifest, write_manifest_atomic, main

def test_pick_sibling_deterministic():
    repos = ["a/one", "a/two", "a/three"]
    assert pick_sibling("xyz", repos) == pick_sibling("xyz", repos)
    assert pick_sibling("xyz", repos) in repos

def test_pick_sibling_never_index_error_empty():
    assert pick_sibling("any", []) is None

def test_pick_sibling_never_index_error_none():
    assert pick_sibling("any", None) is None

def test_build_manifest_filters_by_date_folder():
    tree = {
        "entries": [
            {"path": "2023-10-01/file1.json", "type": "file"},
            {"path": "2023-10-02/file2.json", "type": "file"},
            {"path": "README.md", "type": "file"},
        ]
    }
    manifest = build_manifest(tree, "2023-10-01", "owner/repo")
    paths = [e["path"] for e in manifest["files"]]
    assert "2023-10-01/file1.json" in paths
    assert "2023-10-02/file2.json" not in paths
    assert len(manifest["files"]) >= 1

def test_build_manifest_includes_cdn_urls_no_tokens():
    tree = {"entries": [{"path": "2023-10-01/file1.json", "type": "file"}]}
    manifest = build_manifest(tree, "2023-10-01", "owner/repo")
    for f in manifest["files"]:
        assert "cdn" in f["url"].lower() or "hf.co" in f["url"]
        assert "token" not in f["url"].lower()
        assert "HF_TOKEN" not in f["url"]

def test_write_manifest_atomic_creates_valid_json():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "manifest.json"
        data = {"files": [{"path": "a", "url": "https://cdn.example/a"}]}
        write_manifest_atomic(p, data)
        assert p.exists()
        loaded = json.loads(p.read_text())
        assert loaded == data

def test_write_manifest_atomic_tempfile_removed_on_success():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "manifest.json"
        data = {"files": []}
        write_manifest_atomic(p, data)
        temps = list(Path(td).glob("*.tmp*"))
        assert len(temps) == 0

@mock.patch("discovery_001.fetch_repo_tree")
@mock.patch("discovery_001.write_manifest_atomic")
@mock.patch("discovery_001.check_studio_and_reuse")
def test_main_success_exit0(mock_studio, mock_write, mock_fetch):
    mock_fetch.return_value = {"entries": [{"path": "2023-10-01/f.json", "type": "file"}]}
    mock_write.return_value = None
    mock_studio.return_value = None
    with mock.patch.dict(os.environ, {"HF_TOKEN": "x", "DATE_FOLDER": "2023-10-01", "MANIFEST_DIR": tempfile.mkdtemp()}):
        with pytest.rai
