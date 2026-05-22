import argparse
import sys
from typing import Callable

def _dispatch(args: argparse.Namespace) -> int:
    """
    Dispatch to the selected sub‑command. Each sub‑command registers a
    callable under the `_func` attribute.
    """
    if hasattr(args, "_func"):
        return args._func(args)  # type: ignore
    else:
        print("Error: no sub‑command specified.", file=sys.stderr)
        return 1


def main(argv: list[str] | None = None) -> None:
    """
    Entry point for the `surrogate` CLI.
    """
    parser = argparse.ArgumentParser(
        prog="surrogate",
        description="Surrogate‑1 command‑line utilities."
    )
    subparsers = parser.add_subparsers(title="sub‑commands", dest="command")

    # Register sub‑commands.
    from .format import build_parser as format_parser
    format_parser(subparsers)

    # Parse arguments and dispatch.
    args = parser.parse_args(argv)
    exit_code = _dispatch(args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()