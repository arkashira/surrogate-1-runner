import json
import os
from pathlib import Path
from typing import Any, Dict, List

class TestConfigManager:
    """
    CRUD helper for JSON test configuration files.
    All configs live under `config_path` (default: <repo>/ci_cd_pipelines/test_configs).
    """

    def __init__(self, config_path: str | Path | None = None):
        self.config_path = Path(config_path or Path.cwd() / "ci_cd_pipelines" / "test_configs")
        self.config_path.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ CRUD
    def _full_path(self, name: str) -> Path:
        return self.config_path / f"{name}.json"

    def save_config(self, name: str, data: Dict[str, Any]) -> None:
        with self._full_path(name).open("w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=4, sort_keys=True)

    def load_config(self, name: str) -> Dict[str, Any]:
        with self._full_path(name).open("r", encoding="utf-8") as fp:
            return json.load(fp)

    def update_config(self, name: str, updates: Dict[str, Any]) -> None:
        cfg = self.load_config(name)
        cfg.update(updates)
        self.save_config(name, cfg)

    def delete_config(self, name: str) -> None:
        try:
            self._full_path(name).unlink()
        except FileNotFoundError:
            pass

    def list_configs(self) -> List[str]:
        return [p.stem for p in self.config_path.glob("*.json")]

    # ------------------------------------------------------------------ helpers
    def exists(self, name: str) -> bool:
        return self._full_path(name).is_file()