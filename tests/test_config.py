import os
import pathlib
import tempfile

import pytest

from src import config


def test_load_config_without_file_returns_defaults():
    cfg = config.load_config()
    assert cfg.mysql is None
    assert cfg.mariadb is None


def test_load_config_with_valid_yaml(tmp_path: pathlib.Path):
    yaml_content = """
    mysql:
      connection_string: "mysql://user:pass@localhost:3306/db1"
    mariadb:
      connection_string: "mariadb://user:pass@localhost:3306/db2"
    """
    cfg_path = tmp_path / "valid.yaml"
    cfg_path.write_text(yaml_content, encoding="utf-8")

    cfg = config.load_config(str(cfg_path))
    assert cfg.mysql is not None
    assert cfg.mysql.connection_string == "mysql://user:pass@localhost:3306/db1"
    assert cfg.mariadb is not None
    assert cfg.mariadb.connection_string == "mariadb://user:pass@localhost:3306/db2"


def test_load_config_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        config.load_config("/nonexistent/path.yaml")


def test_load_config_invalid_connection_string_raises(tmp_path: pathlib.Path):
    yaml_content = """
    mysql:
      connection_string: "not-a-valid-dsn"
    """
    cfg_path = tmp_path / "bad.yaml"
    cfg_path.write_text(yaml_content, encoding="utf-8")

    with pytest.raises(ValueError) as excinfo:
        config.load_config(str(cfg_path))
    assert "mysql.connection_string' is not a valid MySQL/MariaDB DSN" in str(excinfo.value)