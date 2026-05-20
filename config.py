"""
Configuration module for surrogate-1 cost optimization integrations.
"""

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class CostForecastConfig:
    """Configuration for the cost forecasting service."""
    endpoint: str
    api_key: str
    timeout_seconds: int = 10


@dataclass(frozen=True)
class AnomalyDetectionConfig:
    """Configuration for the anomaly detection service."""
    endpoint: str
    api_key: str
    timeout_seconds: int = 10


@dataclass(frozen=True)
class RecommendationsConfig:
    """Top-level configuration for the recommendations pipeline."""
    cost_forecast: CostForecastConfig
    anomaly_detection: AnomalyDetectionConfig
    forecast_horizon_days: int = 7
    anomaly_threshold_usd: float = 50.0
    # NEW: Configurable threshold for proactive recommendations
    proactive_cost_threshold_usd: float = 500.0


def load_config() -> RecommendationsConfig:
    """Load configuration from environment variables."""
    cost_endpoint = os.getenv("COST_FORECAST_ENDPOINT", "https://api.example.com/forecast")
    cost_key = os.getenv("COST_FORECAST_API_KEY", "")
    anomaly_endpoint = os.getenv("ANOMALY_DETECTION_ENDPOINT", "https://api.example.com/anomaly")
    anomaly_key = os.getenv("ANOMALY_DETECTION_API_KEY", "")

    horizon = int(os.getenv("FORECAST_HORIZON_DAYS", "7"))
    threshold = float(os.getenv("ANOMALY_THRESHOLD_USD", "50.0"))
    proactive_threshold = float(os.getenv("PROACTIVE_COST_THRESHOLD_USD", "500.0"))

    return RecommendationsConfig(
        cost_forecast=CostForecastConfig(
            endpoint=cost_endpoint,
            api_key=cost_key,
        ),
        anomaly_detection=AnomalyDetectionConfig(
            endpoint=anomaly_endpoint,
            api_key=anomaly_key,
        ),
        forecast_horizon_days=horizon,
        anomaly_threshold_usd=threshold,
        proactive_cost_threshold_usd=proactive_threshold,
    )