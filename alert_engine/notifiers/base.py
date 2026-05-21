from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol

from ..metrics import Metrics
from ..config import ThresholdConfig


class AlertPayload(Protocol):
    metric_name: str
    current_value: float
    baseline_value: float
    diff_percent: float
    threshold_percent: float
    regression_type: str
    timestamp: datetime
    threshold_config: ThresholdConfig


class Notifier(ABC):
    @abstractmethod
    def send(self, payload: AlertPayload) -> bool:
        """Return True if the alert was sent successfully."""