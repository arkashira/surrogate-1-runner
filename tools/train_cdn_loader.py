import json
import requests
from pathlib import Path
from typing import Iterator, Dict

def download_cdn(url: str, dest: Path) -> Path:
    resp = requests.get(url)
    resp.raise_for_status()
    dest.write_bytes(resp.content)
    return dest

def project_row(raw: Dict[str, str]) -> Dict[str, str]:
    return {
        "prompt": raw.get("prompt", ""),
        "response": raw.get("response", ""),
    }

def stream_manifest(manifest_path: Path) -> Iterator[Dict[str, str]]:
    manifest = json.loads(manifest_path.read_text())
    for entry in manifest["files"]:
        url = entry["cdn_url"]
        suffix = Path(url).suffix.lower()
        with Path(tempfile.mkdtemp()) / f"file{suffix}" as p:
            download_cdn(url, p)
            if suffix == ".parquet":
                # Handle parquet files
                pass
            elif suffix in {".jsonl", ".json"}:
                for line in p.read_text().splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    row = json.loads(line)
                    yield project_row(row)

# Example usage
manifest_path = Path("file_manifest.json")
for row in stream_manifest(manifest_path):
    # Process row
    pass