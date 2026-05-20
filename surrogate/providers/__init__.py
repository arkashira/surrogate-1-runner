from importlib import import_module
from typing import Dict, Type
from .base import BaseProvider

_registry: Dict[str, Type[BaseProvider]] = {}

def register(name: str, cls: Type[BaseProvider]) -> None:
    _registry[name.lower()] = cls

def get_provider(name: str) -> Type[BaseProvider]:
    try:
        return _registry[name.lower()]
    except KeyError as exc:                     # pragma: no‑cover
        raise ValueError(f"Unsupported provider: {name}") from exc

# Auto‑register built‑ins
for _mod in ("openai", "anthropic", "huggingface", "google"):
    import_module(f".{_mod}", package=__name__)   # each module calls register()