import json
from pathlib import Path
from typing import Dict

# Adjust this if your config directory lives elsewhere
CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "llm_provider.json"


class LLMProviderConfig:
    """
    Centralised, persisted configuration for all LLM providers.
    - Loads once on import.
    - Provides getters, setters and automatic persistence.
    - Validates that every provider defines both `api_key` and `model_name`.
    """

    _config: Dict[str, Dict[str, str]] = {}

    @classmethod
    def _load_file(cls) -> Dict[str, Dict[str, str]]:
        if not CONFIG_PATH.is_file():
            raise FileNotFoundError(f"LLM provider config not found at {CONFIG_PATH}")

        with CONFIG_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)

        # ---- validation -------------------------------------------------
        for provider, settings in data.items():
            missing = [k for k in ("api_key", "model_name") if k not in settings]
            if missing:
                raise ValueError(
                    f"Provider '{provider}' missing required fields: {', '.join(missing)}"
                )
        # -----------------------------------------------------------------
        return data

    @classmethod
    def load(cls) -> None:
        """Populate the in‑memory cache (called automatically on first use)."""
        cls._config = cls._load_file()

    @classmethod
    def _ensure_loaded(cls) -> None:
        if not cls._config:
            cls.load()

    # -----------------------------------------------------------------
    # Public getters
    @classmethod
    def get_api_key(cls, provider: str) -> str:
        cls._ensure_loaded()
        return cls._config.get(provider, {}).get("api_key", "")

    @classmethod
    def get_model_name(cls, provider: str) -> str:
        cls._ensure_loaded()
        return cls._config.get(provider, {}).get("model_name", "")

    # -----------------------------------------------------------------
    # Mutators – useful for CLI tools or admin UIs
    @classmethod
    def set_provider(cls, provider: str, api_key: str, model_name: str) -> None:
        """Update a provider in‑memory and write the change back to disk."""
        cls._config[provider] = {"api_key": api_key, "model_name": model_name}
        cls._persist()

    @classmethod
    def _persist(cls) -> None:
        """Write the current in‑memory dict back to the JSON file."""
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with CONFIG_PATH.open("w", encoding="utf-8") as f:
            json.dump(cls._config, f, indent=2, sort_keys=True)


# Load eagerly so other modules can rely on it immediately.
LLMProviderConfig.load()