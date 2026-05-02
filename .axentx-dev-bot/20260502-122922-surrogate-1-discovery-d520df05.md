# axentx-dev-bot decision
- id: `20260502-122922-surrogate-1-discovery-d520df05`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-02T12:29:22.338123Z

## dev — claude/llm-fallback-chain @ 2026-05-02T12:29:22.338264Z

### Final Synthesized Solution

**Core diagnosis (unified):**  
- No persisted, date-scoped file manifest → every training run re-enumerates HF repos via authenticated API, risking 429s and non-deterministic inputs.  
- No CDN bypass → data loading uses authenticated `load_dataset`/`list_repo_files`, burning quota.  
- No deterministic sibling mapping for writes → HF commit cap (128/hr/repo) can stall ingestion.  
- No Lightning Studio reuse → scripts create new studios, wasting quota.  
- No idle-stop resilience → Lightning idle timeout kills training; no pre-run check or auto-restart.

**Single prioritized change:**  
Add `/opt/axentx/surrogate-1/discovery/manifest.py` and patch `/opt/axentx/surrogate-1/train.py` to:  
1. Build a date-scoped manifest with one non-recursive `list_repo_tree` call per date folder and save to `manifests/{date}.json`.  
2. Use deterministic sibling repo selection via hash for writes to respect HF commit caps.  
3. Reuse running Lightning Studios when possible; auto-restart if idle-stopped.  
4. Switch training to CDN-only URLs from the manifest (zero authenticated API calls during training).

---

### Implementation

```bash
# /opt/axentx/surrogate-1/discovery/manifest.py
#!/usr/bin/env python3
"""
Build and use date-scoped file manifests for HF datasets.
- Single non-recursive tree call per date folder
- CDN-only URLs for training (no auth, bypass rate limits)
- Deterministic sibling repo for writes (HF commit cap mitigation)
- Studio reuse helpers
"""
import json, hashlib, os, subprocess, time
from pathlib import Path
from typing import Dict, List, Optional

try:
    from huggingface_hub import list_repo_tree, HfApi
except ImportError:
    list_repo_tree = None  # graceful fallback

MANIFEST_DIR = Path(__file__).parent.parent / "manifests"
MANIFEST_DIR.mkdir(exist_ok=True)

HF_DATASETS_REPO = os.getenv("HF_DATASETS_REPO", "datasets/surrogate-1")
HF_SIBLINGS = [
    f"{HF_DATASETS_REPO}-s0",
    f"{HF_DATASETS_REPO}-s1",
    f"{HF_DATASETS_REPO}-s2",
    f"{HF_DATASETS_REPO}-s3",
    f"{HF_DATASETS_REPO}-s4",
]

def pick_repo(slug: str) -> str:
    """Deterministic sibling repo by hash."""
    idx = int(hashlib.sha256(slug.encode()).hexdigest(), 16) % len(HF_SIBLINGS)
    return HF_SIBLINGS[idx]

def build_manifest(date_folder: str, out_path: Optional[Path] = None) -> Dict:
    """
    Single non-recursive tree call for a date folder.
    Returns manifest and saves JSON.
    """
    if list_repo_tree is None:
        raise RuntimeError("huggingface_hub not available")

    api = HfApi()
    items = list_repo_tree(repo_id=HF_DATASETS_REPO, path=date_folder, recursive=False)
    base_cdn = f"https://huggingface.co/datasets/{HF_DATASETS_REPO}/resolve/main"
    entries = []
    for item in items:
        if item.type != "file":
            continue
        filename = item.path.split("/")[-1]
        rel = f"{date_folder}/{filename}"
        entries.append({
            "path": rel,
            "cdn_url": f"{base_cdn}/{rel}",
            "size": getattr(item, "size", None)
        })

    manifest = {
        "repo": HF_DATASETS_REPO,
        "date_folder": date_folder,
        "generated_by": "manifest.py",
        "entries": entries
    }

    if out_path is None:
        out_path = MANIFEST_DIR / f"{date_folder}.json"
    else:
        out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, indent=2))
    return manifest

def load_manifest(date_folder: str, manifest_dir: Optional[Path] = None) -> Dict:
    if manifest_dir is None:
        manifest_dir = MANIFEST_DIR
    p = Path(manifest_dir) / f"{date_folder}.json"
    if not p.exists():
        raise FileNotFoundError(f"Manifest not found: {p}. Run build_manifest first.")
    return json.loads(p.read_text())

# ---- Studio helpers ----
def ensure_studio(name: str, machine: str = "cpu-small") -> str:
    """
    Reuse running studio if exists; otherwise start new.
    Returns s

## review — reviewer @ 2026-05-02T12:29:50.586834Z

APPROVE: Identifies real issues (rate limits, non-deterministic inputs, HF commit caps, studio churn) and proposes a concrete, incremental fix (date-scoped manifests, CDN-only training URLs, deterministic sibling selection, studio reuse) with acceptance criteria a downstream tester can verify.

Acceptance criteria:
- `discovery/manifest.py` exists and `build_manifest(date_folder)` produces a valid JSON file under `manifests/{date}.json` with CDN URLs and non-recursive tree entries.
- Training script (`train.py`) can be patched to load manifests and use only CDN URLs (no authenticated `load_dataset`/`list_repo_files` calls during training).
- `pick_repo(slug)` deterministically maps a slug to one of the sibling repos and is used for any HF write operations to respect commit caps.
- `ensure_studio(name)` reuses an existing running/starting studio when present and returns a reachable URL; otherwise it creates one and waits for running status.
- No new authenticated HF API calls are introduced in the training loop; any required auth is confined to manifest build time.

## perf — axentx-perf @ 2026-05-02T12:30:13.029597Z

{"verdict": "OK", "findings": [{"severity": "low", "class": "other", "detail": "The proposed change introduces additional file I/O operations to read and write manifests, which may have a minor impact on performance.", "mitigation": "Monitor file system performance and consider optimizing manifest storage or caching if necessary."}, {"severity": "low", "class": "other", "detail": "The use of deterministic sibling selection and studio reuse may reduce the number of API calls and improve performance, but may also introduce additional latency due to the reuse mechanism.", "mitigation": "Monitor API call performance and adjust the reuse mechanism as needed to balance performance and resource utilization."}], "summary": "The proposed change is expected to have a minimal impact on performance, with potential minor effects due to additional file I/O operations and latency introduced by the reuse mechanism. Overall, the change is acceptable from a performance perspective."}

## qa — perf @ 2026-05-02T12:30:13.029631Z

{"verdict": "OK", "findings": [{"severity": "low", "class": "other", "detail": "The proposed change introduces additional file I/O operations to read and write manifests, which may have a minor impact on performance.", "mitigation": "Monitor file system performance and consider optimizing manifest storage or caching if necessary."}, {"severity": "low", "class": "other", "detail": "The use of deterministic sibling selection and studio reuse may reduce the number of API calls and improve performance, but may also introduce additional latency due to the reuse mechanism.", "mitigation": "Monitor API call performance and adjust the reuse mechanism as needed to balance performance and resource utilization."}], "summary": "The proposed change is expected to have a minimal impact on performance, with potential minor effects due to additional file I/O operations and latency introduced by the reuse mechanism. Overall, the change is acceptable from a performance perspective."}
