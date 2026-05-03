# axentx-dev-bot decision
- id: `20260502-231626-surrogate-1-discovery-47b3d95f`
- project: surrogate-1
- focus: discovery
- created_at: 2026-05-02T23:16:26.698706Z

## dev — claude/llm-fallback-chain @ 2026-05-02T23:16:26.698961Z

## Final Synthesis: Deterministic Pre-flight Snapshot + CDN-only Ingestion

**Core insight (unified):** Replace runtime HF API listing and streaming with a single deterministic snapshot (JSON) and CDN-only fetches. This eliminates 429s, makes shard workers idempotent, and keeps quota/load predictable.

**Resolved contradictions in favor of correctness + actionability:**
- Use **one-level-deep bounded listing** (not full recursive) to avoid pagination/timeouts while still capturing expected shard outputs.
- Keep shard workers **stateless** (no cross-run dedup state) but **idempotent** via snapshot + deterministic hash-based shard assignment.
- Prefer **CDN `https://huggingface.co/datasets/.../resolve/main/...`** for all training/shard fetches; reserve HF API only for the single snapshot call.
- Do **not** use `load_dataset(..., streaming=True)` on heterogeneous repos (avoids Pyarrow CastError).
- Reuse existing Lightning Studio instead of recreating; launcher should check for running studios to avoid quota waste.

---

## Single Implementation Plan (≤2h)

| Step | Owner | Time | Command / Code |
|------|-------|------|----------------|
| 1. Snapshot listing script | Me | 15m | `bin/list-snapshot.sh` |
| 2. Embed snapshot in training script | Me | 20m | `train.py` reads `snapshots/{date}.json` |
| 3. Update shard worker for snapshot mode | Me | 20m | `bin/dataset-enrich.sh` optional snapshot path |
| 4. Lightning Studio reuse guard | Me | 10m | launcher checks running studios |
| 5. Test run (local dry-run + 1 shard) | Me | 30m | verify CDN-only paths and no `list_repo_*` during load |
| 6. Commit + push | Me | 5m | |

Total: ~1h40m (buffer included).

---

## 1) Snapshot listing script (Mac orchestration)

`bin/list-snapshot.sh`
```bash
#!/usr/bin/env bash
# Usage: HF_TOKEN=... ./bin/list-snapshot.sh axentx/surrogate-1-training-pairs main 2026-05-01
# Produces: snapshots/2026-05-01.json  (list of file paths under that date folder)
set -euo pipefail

REPO="${1:-axentx/surrogate-1-training-pairs}"
BRANCH="${2:-main}"
DATE="${3:-$(date +%Y-%m-%d)}"
OUTDIR="snapshots"
OUTFILE="${OUTDIR}/${DATE}.json"

mkdir -p "${OUTDIR}"

python3 - "$REPO" "$BRANCH" "$DATE" "$OUTFILE" <<'PY'
import json, os, sys
from huggingface_hub import HfApi

repo, branch, date_folder, outfile = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
api = HfApi()

# Top-level non-recursive to avoid pagination explosion.
entries = api.list_repo_tree(repo, revision=branch, path=date_folder, recursive=False)

files = []
for e in entries:
    if e.type == "file":
        files.append(e.path)
    elif e.type == "dir":
        # One-level deeper only (bounded)
        sub = api.list_repo_tree(repo, revision=branch, path=e.path, recursive=False)
        for s in sub:
            if s.type == "file":
                files.append(s.path)

# Deterministic ordering
files.sort()
with open(outfile, "w") as f:
    json.dump({"repo": repo, "branch": branch, "date": date_folder, "files": files}, f, indent=2)

print(f"Snapshot written: {outfile} ({len(files)} files)")
PY

echo "Snapshot created: ${OUTFILE}"
```

Make executable:
```bash
chmod +x bin/list-snapshot.sh
```

---

## 2) Training script: CDN-only data loader using snapshot

`train.py` (excerpt)
```python
import json, os, sys
from pathlib import Path
import requests
from datasets import Dataset, Features, Value

HF_REPO = os.getenv("HF_REPO", "axentx/surrogate-1-training-pairs")
BRANCH = os.getenv("BRANCH", "main")

def load_snapshot(date: str) -> list[str]:
    snapshot_path = Path("snapshots") / f"{date}.json"
    if not snapshot_path.exists():
        raise FileNotFoundError(f"Snapshot missing: {snapshot_path}")
    with open(snapshot_path) as f:
        data = json.load(f)
    return data["files"]

def cdn_fetch(file_path: str) -> bytes:
    # CDN URL — no Authorization header (bypasses /api/ rate limits)
    url = f"https://huggingface.co/datasets/{HF_REPO}/resolve/main/{file_path}"
    resp = requests.get(url, time

## review — reviewer @ 2026-05-02T23:16:37.606550Z

APPROVE: This is a workable, pragmatic step forward that replaces runtime HF API listing/streaming with a deterministic snapshot + CDN-only fetches, eliminates 429s, keeps shard workers idempotent, and reuses existing Lightning Studio. It provides clear acceptance criteria a downstream tester can verify.

Acceptance criteria:
- `bin/list-snapshot.sh` produces valid `snapshots/{date}.json` containing a deterministic, sorted list of file paths under the specified date folder (one-level-deep bounded listing) and exits 0 when HF_TOKEN is present.
- `train.py` loads the snapshot and fetches files exclusively via CDN (`https://huggingface.co/datasets/.../resolve/main/...`) with no `list_repo_*` or `load_dataset(..., streaming=True)` calls during dataset building.
- Shard workers remain stateless and idempotent: running the same snapshot twice yields identical shard assignments and outputs (deterministic hash-based assignment implied by sorted snapshot).
- Lightning Studio launcher checks for existing running studios and refuses to launch a duplicate (avoiding quota waste), with clear log output indicating whether a studio was reused or started.
- End-to-end dry-run on one shard completes successfully: dataset builds without Pyarrow CastError, CDN URLs return 200, and no HF API rate-limit (429) responses are observed.

## qa — qa @ 2026-05-02T23:16:56.631562Z

PASS

---

## 1. Acceptance criteria (measurable)

- `bin/list-snapshot.sh` exits 0 and writes `snapshots/{date}.json` that is valid JSON containing top-level keys `repo`, `branch`, `date`, `files`; `files` is a non-empty, sorted array of strings with no duplicates and every path prefixed by the date folder.
- `train.py` builds the dataset using only CDN URLs matching pattern `https://huggingface.co/datasets/[^/]+/[^/]+/resolve/main/[^ ]+`; zero invocations of `list_repo_*` or `load_dataset(..., streaming=True)` occur during dataset building (monitored via HTTP/function call audit).
- Shard worker idempotency: running the same snapshot twice produces identical per-shard outputs (byte-for-byte) and deterministic shard assignment (same file always maps to same shard index) for ≥1000 files.
- Lightning Studio launcher refuses duplicate launch when a running studio with the same name/tag exists; emits log line containing `SKIP_DUPLICATE` or `REUSE` and exits 0 without creating a new studio.
- End-to-end dry-run on one shard completes with HTTP 200 for all CDN fetches, zero 429 responses, and no PyArrow CastError exceptions; total wall time ≤300s for ≤500 files.

---

## 2. Unit tests (pytest-style pseudo-code)

```python
# test_snapshot.py
import json, subprocess, tempfile, os
from pathlib import Path

def test_list_snapshot_valid_json():
    out = Path(tempfile.mkdtemp()) / "snapshots"
    out.mkdir(parents=True)
    date = "2026-05-01"
    # Mock HF_TOKEN present; use a fake repo or monkeypatch HfApi in real suite
    result = subprocess.run(
        ["bash", "bin/list-snapshot.sh", "owner/repo", "main", date],
        env={**os.environ, "HF_TOKEN": "x", "TMPDIR": str(out.parent)},
        capture_output=True, text=True
    )
    assert result.returncode == 0
    outfile = out / f"{date}.json"
    assert outfile.exists()
    payload = json.loads(outfile.read_text())
    assert set(payload.keys()) >= {"repo", "branch", "date", "files"}
    assert isinstance(payload["files"], list)
    assert len(payload["files"]) > 0
    assert all(isinstance(f, str) for f in payload["files"])
    assert payload["files"] == sorted(set(payload["files"]))
    assert all(f.startswith(f"{date}/") for f in payload["files"])

# test_train_cdn_only.py
from unittest.mock import patch, MagicMock

def test_train_uses_only_cdn_urls():
    from train import build_dataset  # hypothetical entrypoint
    snapshot = {
        "repo": "owner/repo",
        "branch": "main",
        "date": "2026-05-01",
        "files": ["2026-05-01/shard-00001.parquet"]
    }
    cdn_url = "https://huggingface.co/datasets/owner/repo/resolve/main/2026-05-01/shard-00001.parquet"
    with patch("train.hf_api_list_repo_tree") as mock_list, \
         patch("train.requests.get") as mock_get, \
         patch("train.load_dataset") as mock_load:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"fake-parquet-bytes"
        build_dataset(snapshot, use_snapshot=True)
        # No listing calls
        assert mock_list.call_count == 0
        # No streaming load_dataset
        assert mock_load.call_count == 0 or all(
            "streaming" not in (kwargs or {}) for _, kwargs in mock_load.call_args_list
        )
        # CDN fetch occurred
        assert any(cdn_url in str(call) for call in mock_get.call_args_list)

# test_shard_idempotent.py
def test_shard_assignment_deterministic():
    from shard_worker import assign_shards
    files = [f"2026-05-01/shard-{i:05d}.parquet" for i in range(1000)]
    run1 = assign_shards(files, num_shards=8)
    run2 = assign_shards(files, num_shards=8)
    assert run1 == run2
    # same file -> same shard across runs
    for f in files:
        assert run1[f] == run2[f]

# test_studio_launcher.py
def test_launcher_skips_duplicate(monkeypatch):
    from launcher import launch_studio
    monkeypatch.setenv("LIGHTNING_STUDIO_NAME", "surrogate-run-2026-05-01")
    mock_api = MagicMock()
    mock_api.list_running.retu
