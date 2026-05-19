from __future__ import annotations
import json
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional, Tuple

# --------------------------------------------------------------------------- #
# 1.1  Enums
# --------------------------------------------------------------------------- #
class ScenarioType(str, Enum):
    NORMAL = "normal"
    HIGH_ERROR_RATE = "high_error_rate"
    LATENCY_SPIKE = "latency_spike"
    MEMORY_LEAK = "memory_leak"
    CPU_SPIKE = "cpu_spike"
    TRAFFIC_SURGE = "traffic_surge"
    TRAFFIC_DROP = "traffic_drop"
    MIXED = "mixed"


class MetricType(str, Enum):
    GAUGE = "gauge"
    COUNT = "count"
    RATE = "rate"
    HISTOGRAM = "histogram"


# --------------------------------------------------------------------------- #
# 1.2  Service / Metric / Scenario Configs
# --------------------------------------------------------------------------- #
@dataclass
class ServiceConfig:
    name: str
    environment: str = "production"
    version: str = "1.0.0"
    enabled: bool = True
    tags: Dict[str, str] = field(default_factory=dict)

    def to_datadog_tags(self) -> List[str]:
        tags = [
            f"service:{self.name}",
            f"env:{self.environment}",
            f"version:{self.version}",
        ]
        tags.extend(f"{k}:{v}" for k, v in self.tags.items())
        return tags


@dataclass
class MetricConfig:
    name: str
    metric_type: MetricType = MetricType.GAUGE
    interval: int = 10          # seconds
    min_value: float = 0.0
    max_value: float = 100.0
    mean_value: float = 50.0
    std_dev: float = 10.0
    tags: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if isinstance(self.metric_type, str):
            self.metric_type = MetricType(self.metric_type)


@dataclass
class ScenarioConfig:
    scenario_type: ScenarioType
    duration_seconds: int = 300
    intensity: float = 1.0      # 0.0 .. 1.0
    custom_parameters: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if isinstance(self.scenario_type, str):
            self.scenario_type = ScenarioType(self.scenario_type)

    @classmethod
    def from_preset(cls, preset: str, **kwargs) -> "ScenarioConfig":
        mapping = {
            "normal": ScenarioType.NORMAL,
            "high_error": ScenarioType.HIGH_ERROR_RATE,
            "latency": ScenarioType.LATENCY_SPIKE,
            "memory": ScenarioType.MEMORY_LEAK,
            "cpu": ScenarioType.CPU_SPIKE,
            "surge": ScenarioType.TRAFFIC_SURGE,
            "drop": ScenarioType.TRAFFIC_DROP,
            "mixed": ScenarioType.MIXED,
        }
        return cls(
            scenario_type=mapping.get(preset.lower(), ScenarioType.NORMAL),
            **kwargs,
        )