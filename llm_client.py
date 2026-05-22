import json
import os
from typing import Any, Dict, List, Optional

# Path to the JSON configuration that defines LLM providers.
CONFIG_PATH = os.getenv(
    "LLM_PROVIDERS_CONFIG",
    "/opt/axentx/surrogate-1/providers.json"
)

class ProviderConfig:
    """Simple data holder for a provider's configuration."""

    def __init__(
        self,
        name: str,
        api_key: str,
        endpoint: str,
        default_model: str,
    ) -> None:
        self.name = name
        self.api_key = api_key
        self.endpoint = endpoint
        self.default_model = default_model

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProviderConfig":
        required = ["name", "api_key", "endpoint", "default_model"]
        missing = [k for k in required if k not in data]
        if missing:
            raise ValueError(f"Provider config missing keys: {missing}")
        return cls(
            name=data["name"],
            api_key=data["api_key"],
            endpoint=data["endpoint"],
            default_model=data["default_model"],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "api_key": self.api_key,
            "endpoint": self.endpoint,
            "default_model": self.default_model,
        }

class LLMProvider:
    def __init__(self, name: str, model: str):
        self.name = name
        self.model = model

    def generate_response(self, prompt: str) -> str:
        # Placeholder for the new provider's inference logic
        return f"You are a {self.name} model. You are asked: {prompt}. This is your response."

class ProviderRegistry:
    """Singleton registry that loads provider definitions from JSON."""

    _instance: Optional["ProviderRegistry"] = None

    def __new__(cls) -> "ProviderRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._providers: Dict[str, ProviderConfig] = {}
            cls._instance._load()
        return cls._instance

    def _load(self) -> None:
        """Load provider definitions from the JSON config file."""
        if not os.path.exists(CONFIG_PATH):
            # No config – start with an empty registry.
            return
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid JSON in {CONFIG_PATH}: {exc}") from exc

        if not isinstance(raw, list):
            raise RuntimeError(f"Provider config must be a JSON array, got {type(raw)}")

        for entry in raw:
            try:
                cfg = ProviderConfig.from_dict(entry)
                self._providers[cfg.name] = cfg
            except Exception as exc:
                raise RuntimeError(f"Failed to parse provider entry {entry}: {exc}") from exc

    def list_providers(self) -> List[str]:
        """Return a list of registered provider names."""
        return sorted(self._providers.keys())

    def get(self, name: str) -> ProviderConfig:
        """Retrieve a provider configuration by name."""
        try:
            return self._providers[name]
        except KeyError as exc:
            raise KeyError(f"LLM provider '{name}' is not registered.") from exc

    def add_provider(self, cfg: ProviderConfig) -> None:
        """Add a new provider at runtime and persist to the JSON file."""
        self._providers[cfg.name] = cfg
        self._persist()

    def _persist(self) -> None:
        """Write the current registry back to the JSON config file."""
        data = [p.to_dict() for p in self._providers.values()]
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, sort_keys=True)

def infer(provider_name: str, prompt: str, **kwargs: Any) -> str:
    """
    Perform a stub inference call for the given provider.

    This implementation does **not** call any external API; it simply returns a
    deterministic placeholder string that includes the provider name and the
    prompt. The signature mirrors a real client so that later extensions can
    replace the body without changing callers.

    Args:
        provider_name: Name of the registered provider (must exist in the registry).
        prompt: The user prompt to "process".
        **kwargs: Additional parameters that real providers might accept
                  (e.g., temperature, max_tokens). They are ignored in the stub.

    Returns:
        A placeholder response string.
    """
    registry = ProviderRegistry()
    cfg = registry.get(provider_name)  # validates existence
    provider = LLMProvider(cfg.name, cfg.default_model)
    return provider.generate_response(prompt)

# Example usage:
if __name__ == "__main__":
    provider_name = "minimax"
    prompt = "Hello, world!"
    response = infer(provider_name, prompt)
    print(response)