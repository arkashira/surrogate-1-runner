"""
LLMResponse – a stable, JSON‑serialisable container for language model responses.

This module provides a consistent response object abstraction across different
LLM providers, ensuring uniform handling of text, token usage, and finish reasons.

Fields
------
text: str
    The generated text content from the model.
usage: Dict[str, int]
    Token usage statistics (e.g. {"prompt_tokens": int, "completion_tokens": int,
    "total_tokens": int}).
finish_reason: str
    Reason the model stopped generating (e.g. "stop", "length", "content_filter").

Example
-------
>>> response = LLMResponse(
...     text="Hello, world!",
...     usage={"prompt_tokens": 5, "completion_tokens": 3, "total_tokens": 8},
...     finish_reason="stop"
... )
>>> response.to_dict()
{'text': 'Hello, world!', 'usage': {'prompt_tokens': 5, ...}, 'finish_reason': 'stop'}
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict


@dataclass
class LLMResponse:
    """A consistent response object for all LLM providers."""

    text: str
    usage: Dict[str, Any]
    finish_reason: str

    def to_dict(self) -> Dict[str, Any]:
        """
        Return a plain‑dict representation suitable for JSON serialisation.

        Uses ``asdict`` for robust recursive conversion of nested dataclasses.

        Returns
        -------
        dict
            ``{"text": ..., "usage": ..., "finish_reason": ...}``
        """
        return asdict(self)