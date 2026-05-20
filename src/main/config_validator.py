import yaml
from pathlib import Path
from typing import Dict, Any

# Fields that must be present in the YAML config
REQUIRED_FIELDS = {"api_key", "app_key"}


def load_config(path: str | Path) -> Dict[str, Any]:
    """
    Load a YAML configuration file.

    Args:
        path: Path to the YAML file.

    Returns:
        Parsed configuration as a dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not valid YAML or does not contain a mapping.
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        try:
            cfg = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            raise ValueError(f"Invalid YAML in config file {path}: {exc}") from exc

    if not isinstance(cfg, dict):
        raise ValueError(f"Config file {path} must contain a YAML mapping at the root")

    return cfg


def validate_config(cfg: Dict[str, Any]) -> None:
    """
    Validate that the configuration contains all required fields.

    Args:
        cfg: Configuration dictionary.

    Raises:
        ValueError: If any required field is missing.
    """
    missing = REQUIRED_FIELDS - cfg.keys()
    if missing:
        raise ValueError(f"Missing required config fields: {', '.join(sorted(missing))}")