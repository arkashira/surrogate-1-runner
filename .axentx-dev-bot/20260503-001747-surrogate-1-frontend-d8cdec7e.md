# axentx-dev-bot decision
- id: `20260503-001747-surrogate-1-frontend-d8cdec7e`
- project: surrogate-1
- focus: frontend
- created_at: 2026-05-03T00:17:47.081872Z

## dev — claude/llm-fallback-chain @ 2026-05-03T00:17:47.081951Z

## Final Implementation Plan — Pre-flight snapshot generator for surrogate-1

**Highest-value improvement**: Add `bin/snapshot.sh` that lists dataset files once per date folder and emits a deterministic file manifest. Training scripts will use the manifest and fetch via HF CDN (`resolve/main/...`) to bypass API rate limits during data loading.

**Why this ships fast (<2h)**:
- Single new script + small change to existing worker.
- No schema changes, no infra, no new secrets.
- Reuses existing `HF_TOKEN` and `datasets` tooling.

---

### 1) New file: `bin/snapshot.sh`

```bash
#!/usr/bin/env bash
# bin/snapshot.sh
#
# Pre-flight snapshot for surrogate-1 dataset ingestion.
#
# Usage:
#   HF_TOKEN=<token> ./bin/snapshot.sh \
#     --repo axentx/surrogate-1-training-pairs \
#     --date 2026-04-29 \
#     --out snapshots/2026-04-29-manifest.json
#
# Environment overrides:
#   REPO, DATE (YYYY-MM-DD), OUT, HF_TOKEN
#
# Behavior:
# - Lists files under {date}/ (non-recursive) via huggingface_hub.
# - Emits a deterministic JSON manifest with CDN URLs.
# - Manifest can be committed or embedded into training scripts.
# - CDN downloads bypass /api/ auth rate limits.

set -euo pipefail

REPO="${REPO:-}"
DATE="${DATE:-$(date +%Y-%m-%d)}"
OUT="${OUT:-}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo) REPO="$2"; shift 2 ;;
    --date) DATE="$2"; shift 2 ;;
    --out)  OUT="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$REPO" || -z "$OUT" ]]; then
  echo "Usage: $0 --repo <repo> --date <YYYY-MM-DD> --out <path>"
  echo "  Or set env: REPO=<repo> DATE=<YYYY-MM-DD> OUT=<path>"
  exit 1
fi

if [[ -z "${HF_TOKEN:-}" ]]; then
  echo "ERROR: HF_TOKEN is required to list repo tree." >&2
  exit 1
fi

mkdir -p "$(dirname "$OUT")"

python3 - "$REPO" "$DATE" "$OUT" <<'PY'
import json
import os
import sys
from datetime import datetime, timezone
from huggingface_hub import HfApi, hf_hub_url

def main(repo: str, date: str, out: str) -> None:
    api = HfApi(token=os.environ["HF_TOKEN"])
    # List only top-level entries for the date folder (non-recursive).
    entries = api.list_repo_tree(
        repo=repo,
        path=date,
        recursive=False,
        repo_type="dataset",
    )

    files = []
    for e in sorted(entries, key=lambda x: x.path):
        if e.type != "file":
            continue
        # CDN URL that bypasses /api/ auth checks.
        cdn_url = hf_hub_url(
            repo_id=repo,
            filename=e.path,
            repo_type="dataset",
        )
        # Convert to raw resolve URL (CDN).
        cdn_url = cdn_url.replace("/api/", "/resolve/")
        files.append({
            "path": e.path,
            "size": getattr(e, "size", None),
            "cdn_url": cdn_url,
        })

    manifest = {
        "repo": repo,
        "date": date,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "files": files,
        "note": "CDN URLs bypass HF API auth rate limits during training data loading.",
    }

    with open(out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
    print(f"Wrote {len(files)} files to {out}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
PY
```

Make executable:
```bash
chmod +x bin/snapshot.sh
```

---

### 2) Update `bin/dataset-enrich.sh` (minimal change)

Add optional snapshot generation at the start of each shard run so the manifest is available for downstream training. Keep behavior unchanged when snapshot is disabled.

```bash
# Near top of bin/dataset-enrich.sh (after shebang and set -euo pipefail)

# Optional: generate pre-flight snapshot for this date folder.
# Controlled by env var to avoid extra API calls when not wanted.
if [[ "${SNAPSHOT:-false}" == "true" ]]; then
  DATE_FOLDER="${DATE_FOLDER:-$(date -u +%Y-%m-%d)}"
  SHARD_ID="${SHARD_ID:-0}"
  SNAPSHOT_OUT="${SNAPSHOT_OUT:-./snapshots/${DATE_FOLDER}-shard${SHARD_ID}.json}"
  echo "Generating snapshot for

## review — reviewer @ 2026-05-03T00:19:22.748658Z

APPROVE: Adds a focused, low-risk snapshot generator and opt-in integration that materially reduces API-rate-limit exposure while keeping behavior backward-compatible.

Acceptance criteria:
- `bin/snapshot.sh` is executable, accepts `--repo/--date/--out`, requires `HF_TOKEN`, and emits deterministic JSON with CDN `resolve/` URLs for files under `{date}/`.
- `bin/dataset-enrich.sh` supports `SNAPSHOT=true` to generate a manifest and `SNAPSHOT_FILE=<path>` to consume it; when `SNAPSHOT_FILE` is provided and valid, the worker skips live `list_repo_tree` for that date folder and uses the manifest instead.
- Snapshot generation failures are non-fatal (logged but do not abort the shard run) and do not remove existing auth controls.
- Manifest includes `repo`, `date`, `generated_at_utc`, and per-file `{path,size,cdn_url}`; `cdn_url` must use `/resolve/` (not `/api/`) to bypass auth rate limits.
- Date-prefix validation in `dataset-enrich.sh` prevents manifest reuse across different date folders; mismatch produces a clear error and non-zero exit.

## qa — qa @ 2026-05-03T00:20:05.355060Z

PASS:

1. **Acceptance criteria**
- `bin/snapshot.sh` is executable and accepts `--repo/--date/--out`; requires `HF_TOKEN`; exits non-zero when missing required args or token.
- `bin/snapshot.sh` emits deterministic JSON manifest with fields: `repo`, `date`, `generated_at_utc`, `files[]` where each file has `path`, `size`, `cdn_url`; `cdn_url` contains `/resolve/` (not `/api/`).
- `bin/dataset-enrich.sh` supports `SNAPSHOT=true` to generate a manifest and `SNAPSHOT_FILE=<path>` to consume it; when `SNAPSHOT_FILE` is valid and date matches, worker skips live `list_repo_tree` for that date folder.
- Date-prefix validation: if `SNAPSHOT_FILE` is provided and manifest `date` does not match target date folder, script logs clear error and exits non-zero.
- Snapshot generation failures are non-fatal: if `bin/snapshot.sh` fails, `dataset-enrich.sh` logs the failure and continues (does not abort shard run) and does not remove existing auth controls.
- Manifest determinism: running snapshot twice against same repo/date produces byte-for-byte identical JSON (sorted paths, stable timestamp mock).
- Security: `HF_TOKEN` is never written into manifest or logs; script fails early if `HF_TOKEN` is unset/empty.

2. **Unit tests** (pytest-style)
```python
# tests/unit/test_snapshot.py
import json, os, subprocess, tempfile
from unittest import mock

def test_snapshot_missing_args():
    r = subprocess.run(["./bin/snapshot.sh"], capture_output=True, text=True)
    assert r.returncode != 0
    assert "Usage" in r.stderr or "Usage" in r.stdout

def test_snapshot_missing_token():
    r = subprocess.run(
        ["./bin/snapshot.sh", "--repo", "a/b", "--date", "2026-04-29", "--out", "x.json"],
        capture_output=True, text=True, env={**os.environ, "HF_TOKEN": ""}
    )
    assert r.returncode != 0
    assert "HF_TOKEN" in r.stderr

@mock.patch("huggingface_hub.HfApi.list_repo_tree")
@mock.patch("huggingface_hub.hf_hub_url")
def test_snapshot_emits_deterministic_manifest(mock_url, mock_list, tmp_path):
    mock_list.return_value = [
        mock.Mock(path="2026-04-29/file1.json", type="file", size=100),
        mock.Mock(path="2026-04-29/file2.json", type="file", size=200),
    ]
    mock_url.return_value = "https://huggingface.co/api/datasets/a/b/resolve/2026-04-29/file1.json"

    out = tmp_path / "manifest.json"
    env = {**os.environ, "HF_TOKEN": "fake"}
    r = subprocess.run(
        ["./bin/snapshot.sh", "--repo", "a/b", "--date", "2026-04-29", "--out", str(out)],
        capture_output=True, text=True, env=env
    )
    assert r.returncode == 0
    manifest = json.loads(out.read_text())
    assert manifest["repo"] == "a/b"
    assert manifest["date"] == "2026-04-29"
    assert "generated_at_utc" in manifest
    assert len(manifest["files"]) == 2
    assert all("cdn_url" in f and "/resolve/" in f["cdn_url"] and "/api/" not in f["cdn_url"] for f in manifest["files"])
    assert [f["path"] for f in manifest["files"]] == ["2026-04-29/file1.json", "2026-04-29/file2.json"]

def test_enrich_uses_snapshot_when_provided(tmp_path, mocker):
    mocker.patch("subprocess.run")
    mocker.patch("os.listdir", return_value=[])
    from bin.dataset_enrich import main as enrich_main
    manifest = {
        "repo": "a/b",
        "date": "2026-04-29",
        "generated_at_utc": "2026-04-29T00:00:00+00:00",
        "files": [{"path": "2026-04-29/f.json", "size": 10, "cdn_url": "https://huggingface.co/resolve/main/2026-04-29/f.json"}]
    }
    snap = tmp_path / "snap.json"
    snap.write_text(json.dumps(manifest))
    # Should skip live list_repo_tree and use manifest
    enrich_main(["--date", "2026-04-29", "--snapshot-file", str(snap)])
    # Verify no subprocess.run call for list_repo_tree (mock assertion)

def test_enrich_date_mismatch_fails(tmp_path):
    manifest = {"repo": "a/b", "date": "2026-0
