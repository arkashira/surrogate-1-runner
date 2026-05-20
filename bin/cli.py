import argparse
import sys
from surrogate.core.review import run_review_engine


def build_parser() -> argparse.ArgumentParser:
    """
    Construct the top‑level argument parser for the surrogate‑1 CLI.

    The parser now includes the ``--all`` / ``--full`` flag which enables
    multi‑issue mode for the review engine.  For fresh installations the
    default behaviour is to run in this mode, matching the acceptance
    criteria.
    """
    parser = argparse.ArgumentParser(
        prog="surrogate-1",
        description="Run the surrogate‑1 review engine.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Example of other common options – keep them if the real project needs them
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to the configuration file.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output.",
    )

    # -----------------------------------------------------------------
    # New flag: --all / --full
    # -----------------------------------------------------------------
    # * ``action='store_true'`` makes the flag set the value to True.
    # * ``default=True`` implements the “new‑install default” requirement.
    # * ``dest='all_issues'`` gives a stable attribute name that the
    #   review engine can consume.
    parser.add_argument(
        "--all",
        "--full",
        dest="all_issues",
        action="store_true",
        default=True,
        help=(
            "Run the review engine in multi‑issue mode, reporting all detected "
            "issues.  This flag is enabled by default for new installations."
        ),
    )

    # Allow the user to explicitly *disable* the default if they want the
    # historic single‑issue behaviour.
    parser.add_argument(
        "--no-all",
        dest="all_issues",
        action="store_false",
        help="Run the review engine in single‑issue mode (historical default).",
    )

    return parser


def main(argv=None) -> int:
    """
    CLI entry point.

    * Parses arguments.
    * Calls the review engine with the appropriate ``multi_issue_mode`` flag.
    * Returns an exit‑code (0 = success, 1 = failure).
    """
    if argv is None:
        argv = sys.argv[1:]

    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        # The review engine expects a boolean named ``multi_issue_mode``.
        run_review_engine(multi_issue_mode=args.all_issues)
    except Exception as exc:                     # pragma: no cover – defensive
        parser.error(f"Failed to run review engine: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())