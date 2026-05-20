"""
Provider‑specific request/response transformation utilities.

The module is deliberately stateless – all functions are pure and
side‑effect free.  This keeps unit‑testing trivial and guarantees that
the public API is deterministic.

Public helpers
--------------
* `transform_request(provider: str, payload: dict) -> dict`
* `parse_response(provider: str, raw: dict) -> dict`

Both helpers raise a `KeyError` if the provider is unknown.
"""

from __future__ import annotations

from typing import Any, Dict, Tuple

# --------------------------------------------------------------------------- #
# Unified response schema
# --------------------------------------------------------------------------- #
UNIFIED_RESPONSE: Dict[str, Any] = {
    "id": None,
    "model": None,
    "choices": [],
    "usage": {},
}

# --------------------------------------------------------------------------- #
# OpenAI
# --------------------------------------------------------------------------- #
def _openai_transform_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    """OpenAI expects `model`, `prompt` (or `messages`) and optional `max_tokens`."""
    return {
        "model": payload["model"],
        "prompt": payload["prompt"],
        "max_tokens": payload.get("max_tokens", 256),
    }


def _openai_parse_response(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Map OpenAI’s response into the unified schema."""
    return {
        "id": raw.get("id"),
        "model": raw.get("model"),
        "choices": raw.get("choices", []),
        "usage": raw.get("usage", {}),
    }


# --------------------------------------------------------------------------- #
# Anthropic
# --------------------------------------------------------------------------- #
def _anthropic_transform_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Anthropic expects `model`, `prompt` (single string) and `max_tokens_to_sample`."""
    return {
        "model": payload["model"],
        "prompt": payload["prompt"],
        "max_tokens_to_sample": payload.get("max_tokens", 256),
    }


def _anthropic_parse_response(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Map Anthropic’s response into the unified schema."""
    return {
        "id": raw.get("id"),
        "model": raw.get("model"),
        "choices": [
            {
                "text": raw.get("completion"),
                "index": 0,
                "finish_reason": raw.get("stop_reason"),
            }
        ],
        "usage": {
            "prompt_tokens": raw.get("prompt_tokens"),
            "completion_tokens": raw.get("completion_tokens"),
            "total_tokens": raw.get("total_tokens"),
        },
    }


# --------------------------------------------------------------------------- #
# Registry
# --------------------------------------------------------------------------- #
_TRANSFORMERS: Dict[
    str, Tuple[callable, callable]
] = {
    "openai": (_openai_transform_request, _openai_parse_response),
    "anthropic": (_anthropic_transform_request, _anthropic_parse_response),
}


def transform_request(provider: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Return the provider‑specific request payload."""
    if provider not in _TRANSFORMERS:
        raise KeyError(f"Unknown provider: {provider}")
    transform_fn, _ = _TRANSFORMERS[provider]
    return transform_fn(payload)


def parse_response(provider: str, raw: Dict[str, Any]) -> Dict[str, Any]:
    """Return the unified response representation."""
    if provider not in _TRANSFORMERS:
        raise KeyError(f"Unknown provider: {provider}")
    _, parse_fn = _TRANSFORMERS[provider]
    return parse_fn(raw)