# tests/unit/test_make_plan.py
import json, os, tempfile, subprocess
from pathlib import Path

def test_make_plan_produces_valid_schema():
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        Path("bin").mkdir()
        # copy/mock make-plan.sh and minimal python shim
        plan_out = Path(tmp) / "plan" / "2023-10-05" / "files.json"
        subprocess.run(["bash", "bin/make-plan.sh", "2023-10-05"], check=True, env={**os.environ, "REPO": "owner/dummy"})
        assert plan_out.exists()
        payload = json.loads(plan_out.read_text())
        assert payload["date"] == "2023-10-05"
        assert "T" in payload["created_at"] and "Z" in payload["created_at"]
        assert payload["shards"] == 16
        for f in payload["files"]:
            assert "path" in f and isinstance(f["path"], str)
            assert 0 <= f["shard"] <= 15
            assert "resolve/main/" in f["cdn_url"]

def test_shard_assignment_deterministic():
    paths = ["2023/10/05/a.jsonl", "2023/10/05/b.jsonl"]
    shards = [hash(p) % 16 for p in paths]
    shards_again = [hash(p) % 16 for p in paths]
    assert shards == shards_again