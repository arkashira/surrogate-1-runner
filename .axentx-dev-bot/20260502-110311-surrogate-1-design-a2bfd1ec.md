# axentx-dev-bot decision
- id: `20260502-110311-surrogate-1-design-a2bfd1ec`
- project: surrogate-1
- focus: design
- created_at: 2026-05-02T11:03:11.658242Z

## dev — claude/llm-fallback-chain @ 2026-05-02T11:03:11.658408Z

## Final synthesized implementation (best of both proposals)

**Core principle:**  
- **Training and frontend must never call HF API during training.**  
- **One deterministic, date-folder-pinned manifest per repo/folder is produced on the Mac (or CI) and embedded/cached.**  
- **All ingestion and training consume only that manifest; CDN URLs are used for file fetches.**  
- **Rate-limit safety: 1 HF list call per folder, then CDN-only; ingestion shard routing is deterministic to avoid 128/hr/repo hot-spots.**

---

### 1. Mac/CI orchestration: generate pinned manifest (CLI + lib)

**File:** `/opt/axentx/surrogate-1/scripts/gen-cdn-manifest.py`

```python
#!/usr/bin/env python3
"""
Generate a deterministic, date-folder-pinned CDN manifest.
Usage:
  HF_REPO=datasets/owner/repo FOLDER=2026-05-01 \
  python3 gen-cdn-manifest.py --out ./manifests

Outputs:
  ./manifests/filelist-datasets-owner-repo-2026-05-01.json
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

try:
    from huggingface_hub import list_repo_tree
except ImportError:
    print("Error: huggingface_hub required. pip install huggingface_hub", file=sys.stderr)
    sys.exit(1)

def build_manifest(repo: str, folder: str, output_path: str) -> None:
    # Normalize repo: strip datasets/ prefix for HF API
    repo_id = repo.replace("datasets/", "").strip("/")
    folder = folder.strip("/")

    try:
        tree = list_repo_tree(repo_id, recursive=True, path=folder)
    except Exception as exc:
        print(f"Failed to list {repo_id}@{folder}: {exc}", file=sys.stderr)
        sys.exit(1)

    files = []
    for item in tree:
        if getattr(item, "type", None) != "file":
            continue
        path = item.path
        # Ensure path is absolute within repo
        if not path.startswith(folder):
            path = f"{folder}/{path}" if folder else path
        files.append(
            {
                "path": path,
                "size": int(getattr(item, "size", 0) or 0),
                "sha256": getattr(item, "sha256", None),
                "lastModified": getattr(item, "_last_modified", None)
                or getattr(item, "lastModified", None),
            }
        )

    # Deterministic ordering
    files.sort(key=lambda x: (x["path"], x["size"]))

    manifest = {
        "repo": repo,
        "folder": folder,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "generatedBy": "gen-cdn-manifest.py",
        "files": files,
    }

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True, ensure_ascii=False)

    print(f"Manifest written: {output_path} ({len(files)} files)")

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate pinned CDN manifest for a repo+folder.")
    parser.add_argument("--repo", default=os.getenv("HF_REPO"), help="HF repo (e.g. datasets/owner/repo)")
    parser.add_argument("--folder", default=os.getenv("FOLDER"), help="Date folder (e.g. 2026-05-01)")
    parser.add_argument("--out", default=os.getenv("OUTDIR", "./manifests"), help="Output directory")
    args = parser.parse_args()

    if not args.repo or not args.folder:
        parser.error("Provide --repo and --folder (or set HF_REPO and FOLDER env vars).")

    safe_repo = args.repo.replace("/", "-").replace(" ", "_")
    safe_folder = args.folder.replace("/", "-")
    out_file = os.path.join(args.out, f"filelist-{safe_repo}-{safe_folder}.json")
    build_manifest(args.repo, args.folder, out_file)

if __name__ == "__main__":
    main()
```

**Usage (Mac/CI):**
```bash
pip install huggingface_hub
HF_REPO=datasets/owner/repo FOLDER=2026-05-01 python3 gen-cdn-manifest.py --out ./frontend/public/filelists
```

Place generated manifests into `frontend/public/filelists/` so they are served statically.

---

### 2. Frontend: typed CDN manifest loader (production-r

## review — reviewer @ 2026-05-02T11:35:36.220691Z

APPROVE: 
* The proposed change identifies a real issue with rate limiting and proposes a workable change toward fixing it by generating a deterministic, date-folder-pinned manifest per repo/folder.
* The code/config makes sense, using a CLI tool to generate the manifest and a typed CDN manifest loader in the frontend.
* The implementation is a good first step toward the focus area of design, providing a clear and incremental progress.
* The acceptance criteria for a downstream tester could include:
  * Verifying that the generated manifest is correctly formatted and contains the expected files.
  * Checking that the frontend loader correctly fetches and parses the manifest.
  * Testing that the rate limiting safety mechanism is effective in preventing excessive HF API calls.
  * Confirming that the manifests are correctly placed in the `frontend/public/filelists` directory and served statically.
  * Validating that the TTL and cache key mechanisms are correctly implemented to ensure freshness and consistency of the manifests.

## qa — qa @ 2026-05-02T11:35:49.970756Z

PASS: proposal accepted — deterministic CDN manifest generation and consumption with rate-limit safety.

---

### 1. Acceptance criteria
- Manifest generation produces valid JSON with required fields (repo, folder, generatedAt, generatedBy, files) and ≥1 file entry when HF folder is non-empty.
- Manifest file naming follows deterministic pattern: `filelist-datasets-owner-repo-YYYY-MM-DD.json` and is written to the configured output directory.
- Files list is sorted deterministically by (path, size) and each entry includes path (string), size (non-negative integer), sha256 (string|null), lastModified (ISO8601|null).
- Training/frontend never calls HF API during training: ingestion and training consume only CDN URLs derived from the manifest; any direct HF API call during training raises a runtime error or is blocked by a network policy stub.
- Rate-limit safety: at most one HF list call per (repo, folder) per manifest generation; subsequent runs within TTL reuse cached manifest and do not trigger HF API calls.
- CDN file fetch uses HTTPS URLs constructed from repo/folder/path and returns HTTP 200 for available files; missing files produce 404 and are logged without crashing ingestion.
- Manifest TTL/caching: loader respects TTL (e.g., 24h) and cache key (repo+folder+date) and falls back to last valid manifest on CDN fetch failure without retrying HF API.

---

### 2. Unit tests (pytest-style pseudo-code)

```python
# tests/unit/test_gen_cdn_manifest.py
import json
from unittest import mock
from gen_cdn_manifest import build_manifest

def test_build_manifest_valid_structure(tmp_path):
    out = tmp_path / "manifest.json"
    with mock.patch("gen_cdn_manifest.list_repo_tree") as list_mock:
        list_mock.return_value = [
            mock.Mock(path="2026-05-01/a.parquet", type="file", size=1024, sha256="abc", _last_modified="2026-05-01T00:00:00Z"),
            mock.Mock(path="2026-05-01/b.txt", type="file", size=512, sha256=None, _last_modified=None),
        ]
        build_manifest("datasets/owner/repo", "2026-05-01", str(out))

    manifest = json.loads(out.read_text())
    assert manifest["repo"] == "datasets/owner/repo"
    assert manifest["folder"] == "2026-05-01"
    assert "generatedAt" in manifest
    assert manifest["generatedBy"] == "gen-cdn-manifest.py"
    assert len(manifest["files"]) == 2

def test_files_sorted_deterministically(tmp_path):
    out = tmp_path / "manifest.json"
    with mock.patch("gen_cdn_manifest.list_repo_tree") as list_mock:
        list_mock.return_value = [
            mock.Mock(path="z", type="file", size=1, sha256=None, _last_modified=None),
            mock.Mock(path="a", type="file", size=2, sha256=None, _last_modified=None),
        ]
        build_manifest("datasets/x/y", "", str(out))
    paths = [f["path"] for f in json.loads(out.read_text())["files"]]
    assert paths == sorted(paths)

def test_file_entry_fields_non_negative_size(tmp_path):
    out = tmp_path / "manifest.json"
    with mock.patch("gen_cdn_manifest.list_repo_tree") as list_mock:
        list_mock.return_value = [
            mock.Mock(path="f", type="file", size=0, sha256=None, _last_modified=None),
        ]
        build_manifest("datasets/a/b", "folder", str(out))
    files = json.loads(out.read_text())["files"]
    assert all(f["size"] >= 0 for f in files)
    assert all(isinstance(f["path"], str) for f in files)

def test_build_manifest_empty_folder(tmp_path):
    out = tmp_path / "manifest.json"
    with mock.patch("gen_cdn_manifest.list_repo_tree") as list_mock:
        list_mock.return_value = []
        build_manifest("datasets/empty/repo", "empty", str(out))
    manifest = json.loads(out.read_text())
    assert manifest["files"] == []

# tests/unit/test_cdn_manifest_loader.py
from surrogate1.cdn_manifest_loader import CDNManifestLoader

def test_loader_parses_manifest():
    loader = CDNManifestLoader(ttl_seconds=86400)
    manifest = loader.parse_manifest('{"repo":"datasets/x","folder":"f","generatedAt":"20
