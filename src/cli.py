import argparse
import sys
from .detector import detect_latest
from .dataset.enrich import enrich_dataset

def _cmd_detect(_args: argparse.Namespace) -> int:
    """
    Detect breaking changes against the latest deployment.

    Returns:
        int: 0 → no breaking changes, 1 → breaking changes found
    """
    changes = detect_latest()
    if changes:
        for line in changes:
            print(line)
        return 1
    print("No breaking changes.")
    return 0


def _cmd_enrich(args: argparse.Namespace) -> int:
    """
    Enrich a deterministic shard of the public dataset list.

    Returns:
        int: 0 on success, non‑zero on failure.
    """
    try:
        enrich_dataset(shard_id=args.shard, output_dir=args.output)
        return 0
    except Exception as exc:          # pragma: no cover – defensive
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="s1",
        description="Surrogate‑1 CLI – contract stability detection and utilities."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ---- s1 detect -------------------------------------------------
    detect = subparsers.add_parser(
        "detect",
        help="Detect breaking changes against the latest deployment."
    )
    detect.set_defaults(func=_cmd_detect)

    # ---- s1 enrich -------------------------------------------------
    enrich = subparsers.add_parser(
        "enrich",
        help="Enrich a deterministic 1/16 shard of the public dataset list."
    )
    enrich.add_argument(
        "--shard",
        type=int,
        required=True,
        help="Shard index (0‑15)."
    )
    enrich.add_argument(
        "--output",
        default="output",
        help="Directory where processed datasets will be written."
    )
    enrich.set_defaults(func=_cmd_enrich)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())