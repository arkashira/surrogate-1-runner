"""Configuration management for the cost forecasting system."""

import os
from typing import Dict, List, Any
from dataclasses import dataclass, field


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    url: str = field(default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///forecasts.db"))
    pool_size: int = int(os.getenv("DB_POOL_SIZE", "5"))
    max_overflow: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    pool_timeout: int = int(os.getenv("DB_POOL_TIMEOUT", "30"))


@dataclass
class ForecastingConfig:
    """Forecasting algorithm settings."""
    window_days: int = int(os.getenv("FORECAST_WINDOW_DAYS", "30"))
    accuracy_threshold: float = float(os.getenv("FORECAST_ACCURACY_THRESHOLD", "0.95"))
    update_frequency_hours: int = int(os.getenv("UPDATE_FREQUENCY_HOURS", "24"))
    min_confidence_threshold: float = float(os.getenv("MIN_CONFIDENCE", "0.70"))
    model_version: str = os.getenv("MODEL_VERSION", "v1")


@dataclass
class CostConfig:
    """Cost tracking and alerting configuration."""
    metrics: List[str] = field(default_factory=lambda: [
        "compute_hours",
        "storage_gb", 
        "network_egress_gb",
        "api_calls",
        "data_transfer",
    ])
    
    thresholds: Dict[str, float] = field(default_factory=lambda: {
        "high_cost_alert": 1000.0,
        "optimization_target": 0.15,
        "anomaly_threshold": 2.0,
        "critical_cost_threshold": 5000.0,
        "warning_cost_threshold": 2500.0,
    })


class Config:
    """Main configuration class aggregating all settings."""
    
    def __init__(self):
        self.database = DatabaseConfig()
        self.forecasting = ForecastingConfig()
        self.cost = CostConfig()
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables."""
        return cls()
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of errors."""
        errors = []
        
        if self.forecasting.window_days < 1:
            errors.append("FORECAST_WINDOW_DAYS must be at least 1")
        
        if not 0 < self.forecasting.accuracy_threshold <= 1:
            errors.append("FORECAST_ACCURACY_THRESHOLD must be between 0 and 1")
        
        if self.forecasting.min_confidence_threshold < 0 or self.forecasting.min_confidence_threshold > 1:
            errors.append("MIN_CONFIDENCE must be between 0 and 1")
        
        return errors


# Legacy compatibility - module-level constants
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///forecasts.db")
FORECAST_WINDOW_DAYS = int(os.getenv("FORECAST_WINDOW_DAYS", "30"))
FORECAST_ACCURACY_THRESHOLD = float(os.getenv("FORECAST_ACCURACY_THRESHOLD", "0.95"))
UPDATE_FREQUENCY_HOURS = int(os.getenv("UPDATE_FREQUENCY_HOURS", "24"))

COST_METRICS = [
    "compute_hours",
    "storage_gb",
    "network_egress_gb",
    "api_calls",
    "data_transfer",
]

RECOMMENDATION_THRESHOLDS = {
    "high_cost_alert": 1000.0,
    "optimization_target": 0.15,
    "anomaly_threshold": 2.0,
}