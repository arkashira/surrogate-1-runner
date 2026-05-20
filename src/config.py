import os
import re
from dataclasses import dataclass
from typing import Optional

import yaml

# Simple regex to sanity‑check MySQL/MariaDB DSNs.
_CONNECTION_STRING_REGEX = re.compile(
    r'^(mysql|mariadb)://[^/@\s]+(?::[^/@\s]+)?@[^/:]+(?::\d+)?/[^/\s]+(\?.*)?$',
    re.IGNORECASE,
)


@dataclass(frozen=True)
class DBConfig:
    """Configuration for a single database endpoint."""
    connection_string: str


@dataclass(frozen=True)
class AppConfig:
    """Top‑level configuration loaded from a YAML file."""
    mysql: Optional[DBConfig] = None
    mariadb: Optional[DBConfig] = None


def _validate_connection_string(name: str, value: str) -> None:
    """Raise a ValueError with a clear message if *value* is not a valid DSN."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"'{name}.connection_string' must be a non‑empty string")
    if not _CONNECTION_STRING_REGEX.match(value):
        raise ValueError(
            f"'{name}.connection_string' is not a valid MySQL/MariaDB DSN: {value}"
        )


def _parse_section(section: Optional[dict], name: str) -> Optional[DBConfig]:
    """Parse a single top‑level section (mysql or mariadb)."""
    if section is None:
        return None
    cs = section.get("connection_string")
    _validate_connection_string(name, cs)
    return DBConfig(connection_string=cs)


def load_config(path: Optional[str] = None) -> AppConfig:
    """
    Load configuration from *path* (YAML). If *path* is ``None`` the function
    looks for the ``DBCOMPARE_CONFIG`` environment variable. When no file is
    supplied the function returns an ``AppConfig`` with ``None`` for both
    databases (the tool will fall back to its internal defaults).

    The YAML file must contain optional top‑level ``mysql`` and ``mariadb``
    mappings, each with a ``connection_string`` key.

    Example ``config.yaml``::

        mysql:
          connection_string: "mysql://user:pass@host:3306/dbname"
        mariadb:
          connection_string: "mariadb://user:pass@host:3306/dbname"
    """
    # Resolve path from argument → env var → None
    if path is None:
        path = os.getenv("DBCOMPARE_CONFIG")

    if path:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Config file not found: {path}")
        with open(path, "r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh) or {}
    else:
        raw = {}

    mysql_cfg = _parse_section(raw.get("mysql"), "mysql")
    mariadb_cfg = _parse_section(raw.get("mariadb"), "mariadb")

    return AppConfig(mysql=mysql_cfg, mariadb=mariadb_cfg)