import argparse
import sys

from src import config  # Adjust import path if package layout differs

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dbcompare",
        description="Compare MySQL and MariaDB instances based on a shared config.",
    )
    parser.add_argument(
        "--config",
        type=str,
        help=(
            "Path to a YAML configuration file containing `mysql` and/or `mariadb` "
            "sections. If omitted, the tool will look for the DBCOMPARE_CONFIG "
            "environment variable or fall back to built‑in defaults."
        ),
    )
    # Existing arguments would be added here (e.g., --verbose, sub‑commands, etc.)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        app_cfg = config.load_config(args.config)
    except (FileNotFoundError, ValueError) as exc:
        parser.error(str(exc))

    # At this point ``app_cfg`` holds validated connection strings (or None).
    # The rest of the CLI can use ``app_cfg.mysql`` and ``app_cfg.mariadb``.
    # For demonstration we simply print the resolved configuration.
    if app_cfg.mysql:
        print(f"MySQL DSN: {app_cfg.mysql.connection_string}")
    else:
        print("MySQL DSN: <default>")

    if app_cfg.mariadb:
        print(f"MariaDB DSN: {app_cfg.mariadb.connection_string}")
    else:
        print("MariaDB DSN: <default>")

    # TODO: invoke the actual DB comparison logic here, passing ``app_cfg``.
    return 0


if __name__ == "__main__":
    sys.exit(main())