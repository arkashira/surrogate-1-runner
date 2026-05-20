"""
Model configuration utilities.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class ModelConfig:
    """Configuration for an open‑weight LLM."""
    name: str
    model_id: str          # HuggingFace ID
    max_length: int = 2048
    batch_size: int = 1
    device: str = "cuda"
    dtype: str = "float16"
    quantization: Optional[int] = None  # bits
    description: str = ""

# ---------------------------------------------------------------------------

AVAILABLE_MODELS: Dict[str, ModelConfig] = {
    "llama2-7b": ModelConfig(
        name="Llama 2 7B",
        model_id="meta-llama/Llama-2-7b-hf",
        max_length=4096,
        description="Meta's Llama 2 7B model",
    ),
    "llama2-13b": ModelConfig(
        name="Llama 2 13B",
        model_id="meta-llama/Llama-2-13b-hf",
        max_length=4096,
        description="Meta's Llama 2 13B model",
    ),
    "mistral-7b": ModelConfig(
        name="Mistral 7B",
        model_id="mistralai/Mistral-7B-v0.1",
        max_length=8192,
        description="Mistral AI's 7B model",
    ),
    "mixtral-8x7b": ModelConfig(
        name="Mixtral 8x7B",
        model_id="mistralai/Mixtral-8x7B-v0.1",
        max_length=32768,
        description="Mistral AI's mixture‑of‑experts model",
    ),
    "gemma-7b": ModelConfig(
        name="Gemma 7B",
        model_id="google/gemma-7b",
        max_length=8192,
        description="Google's Gemma 7B model",
    ),
    "qwen-7b": ModelConfig(
        name="Qwen 7B",
        model_id="Qwen/Qwen-7B",
        max_length=8192,
        description="Alibaba's Qwen 7B model",
    ),
    "phi-3-mini": ModelConfig(
        name="Phi‑3 Mini",
        model_id="microsoft/Phi-3-mini-4k-instruct",
        max_length=4096,
        description="Microsoft's Phi‑3 Mini model",
    ),
    "falcon-7b": ModelConfig(
        name="Falcon 7B",
        model_id="tiiuae/falcon-7b",
        max_length=2048,
        description="TII's Falcon 7B model",
    ),
}

def get_available_models() -> Dict[str, ModelConfig]:
    """Return a copy of all available model configs."""
    return AVAILABLE_MODELS.copy()

def get_model(key: str) -> ModelConfig:
    """Retrieve a single model config by key."""
    if key not in AVAILABLE_MODELS:
        raise KeyError(f"Unknown model key: {key}. Available: {list(AVAILABLE_MODELS)}")
    return AVAILABLE_MODELS[key]