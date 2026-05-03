import argparse
import random
from pathlib import Path

from bin.lib.cdn_loader import load_manifest, stream_jsonl_cdn

def build_dataloader_from_snapshot(manifest_path: str, repo: str, seed: int = 42):
    manifest = load_manifest(manifest_path)
    files = sorted(manifest["files"], key=lambda x: x["path"])
    random.Random(seed).shuffle(files)

    def generator():
        for item in files:
            try:
                for record in stream_jsonl_cdn(
                    repo=repo,
                    filepath=item["path"],
                    expected_size=item.get("size"),
                ):
                    yield {
                        "prompt": record.get("prompt") or record.get("input") or "",
                        "response": record.get("response") or record.get("output") or "",
                    }
            except Exception as exc:
                # Log and skip bad shards instead of crashing training
                print(f"Skipping {item['path']}: {exc}")
                continue

    return generator

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", type=str, default=None, help="Path to manifest.json")
    parser.add_argument("--repo", type=str, default="axentx/surrogate-1-training-pairs")
    args = parser.parse_args()

    if args.snapshot:
        gen = build_dataloader_from_snapshot(args.snapshot, args.repo)
        # Example: consume first batch
        for i, item in enumerate(gen):
            if i >= 10:
                break
            print(item)
    else:
        # Legacy path (unchanged)
        from datasets import load_dataset
        ds = load_dataset(args.repo, split="train")
        print("Legacy dataset loaded (no snapshot).")