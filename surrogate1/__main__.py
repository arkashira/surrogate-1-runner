#!/usr/bin/env python
"""Entry point for the Surrogate‑1 command line interface."""
import argparse
import logging
import sys

from .core import run_surrogate1

# Configure root logger once – all modules will inherit
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

def main() -> None:
    parser = argparse.ArgumentParser(description="Run Surrogate‑1")
    parser.add_argument(
        "--secure",
        action="store_true",
        help="Run the tool in secure mode (uses SURROGATE1_API_KEY)",
    )
    args = parser.parse_args()

    if args.secure:
        logging.getLogger(__name__).info("Running in secure mode")
    else:
        logging.getLogger(__name__).info("Running in normal mode")

    # Directly invoke the core logic – no subprocess recursion
    run_surrogate1(secure=args.secure)

if __name__ == "__main__":
    main()