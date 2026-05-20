import argparse
import sys
from review.engine import ReviewEngine, run_review


def build_parser() -> argparse.ArgumentParser:
    """
    Build the ArgumentParser for the surrogate‑1 CLI.
    Returns:
        argparse.ArgumentParser: Configured parser.
    """
    parser = argparse.ArgumentParser(
        description="Surrogate‑1 Review CLI – run the review engine in single‑ or multi‑issue mode."
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run the review engine in multi‑issue mode (primary flag).",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Alias for --all; kept for backward compatibility.",
    )
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """
    Parse a list of command‑line arguments.
    Args:
        argv: List of arguments (defaults to ``sys.argv[1:]``).
    Returns:
        argparse.Namespace with the parsed flags.
    """
    parser = build_parser()
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """
    CLI entry‑point used by ``python -m surrogate-1`` or the installed console script.
    Returns:
        Exit status code (0 = success, non‑zero = error).
    """
    args = parse_args(argv)

    # The engine itself is deliberately lightweight – we instantiate it once here.
    engine = ReviewEngine()

    # Dispatch based on the flags. ``--full`` is an alias for ``--all``.
    if args.all or args.full:
        engine.run_multi_issue_mode()
    else:
        engine.run_single_issue_mode()

    return 0


if __name__ == "__main__":
    sys.exit(main())