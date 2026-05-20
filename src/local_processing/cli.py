import argparse
from pathlib import Path

from .processor import Processor


def main() -> None:
    parser = argparse.ArgumentParser(description="Shard‑aware JSON processor")
    parser.add_argument("--shard-id", type=int, required=True, help="Shard number (0‑based)")
    parser.add_argument("--dataset-path", type=Path, required=True, help="Path to JSON files")
    parser.add_argument("--output-path", type=Path, required=True, help="Where to write processed files")
    parser.add_argument("--md5-store-path", type=Path, required=True, help="Persisted MD5 hash set")
    parser.add_argument("--shard-count", type=int, default=16, help="Total number of shards")
    args = parser.parse_args()

    proc = Processor(
        shard_id=args.shard_id,
        dataset_path=args.dataset_path,
        output_path=args.output_path,
        md5_store_path=args.md5_store_path,
        shard_count=args.shard_count,
    )
    proc.run()


if __name__ == "__main__":
    main()