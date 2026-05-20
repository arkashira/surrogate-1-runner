"""
Watermark Benchmark Suite
=========================

Provides a lightweight, extensible framework for measuring
watermark insertion/verification latency and robustness
across open‑weight LLMs.

Public API
----------
from watermark_bench import (
    ModelConfig,
    get_available_models,
    LatencyBenchmark,
    RobustnessBenchmark,
    BenchmarkRunner,
)
"""

from .models import ModelConfig, get_available_models
from .latency import LatencyBenchmark
from .robustness import RobustnessBenchmark
from .runner import BenchmarkRunner

__all__ = [
    "ModelConfig",
    "get_available_models",
    "LatencyBenchmark",
    "RobustnessBenchmark",
    "BenchmarkRunner",
]