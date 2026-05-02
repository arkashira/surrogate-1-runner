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

## perf — axentx-perf @ 2026-05-02T12:04:24.518319Z

{"verdict": "OK", "findings": [{"severity": "low", "class": "unbounded-query", "detail": "Manifest generation for DATE_FOLDER may list all repo files without pagination/limit; if folder contains many assets this could increase latency and memory during cron runs.", "mitigation": "Cap file count or stream entries; add timeout and size budget for manifest writes."}, {"severity": "low", "class": "sync-in-async", "detail": "If called from async contexts, HF hub calls and filesystem writes are likely blocking; could stall event loop under load.", "mitigation": "Run I/O in threadpool or use async-native hf client and aiofiles."}, {"severity": "low", "class": "memory-leak", "detail": "Manifest kept in memory and logged in full; large manifests may bloat cron logs and process RSS.", "mitigation": "Log summary only; stream JSON to disk and avoid retaining full object post-write."}], "summary": "No high-risk perf issues; acceptable for production with low-severity caveats around unbounded listing, blocking I/O, and log/memory footprint."}

## qa — perf @ 2026-05-02T12:04:24.518355Z

{"verdict": "OK", "findings": [{"severity": "low", "class": "unbounded-query", "detail": "Manifest generation for DATE_FOLDER may list all repo files without pagination/limit; if folder contains many assets this could increase latency and memory during cron runs.", "mitigation": "Cap file count or stream entries; add timeout and size budget for manifest writes."}, {"severity": "low", "class": "sync-in-async", "detail": "If called from async contexts, HF hub calls and filesystem writes are likely blocking; could stall event loop under load.", "mitigation": "Run I/O in threadpool or use async-native hf client and aiofiles."}, {"severity": "low", "class": "memory-leak", "detail": "Manifest kept in memory and logged in full; large manifests may bloat cron logs and process RSS.", "mitigation": "Log summary only; stream JSON to disk and avoid retaining full object post-write."}], "summary": "No high-risk perf issues; acceptable for production with low-severity caveats around unbounded listing, blocking I/O, and log/memory footprint."}
