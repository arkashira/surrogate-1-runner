"""
Centralised configuration for the RecommendationGenerator.
Values are read from environment variables so that secrets never
touch the codebase.
"""

import os
from dataclasses import dataclass, field
from typing import Optional

@dataclass(frozen=True)
class SMTPConfig:
    server: str = field(default_factory=lambda: os.getenv("SMTP_SERVER", "smtp.example.com"))
    port: int = field(default_factory=lambda: int(os.getenv("SMTP_PORT", 587)))
    username: str = field(default_factory=lambda: os.getenv("SMTP_USERNAME", "user@example.com"))
    password: str = field(default_factory=lambda: os.getenv("SMTP_PASSWORD", "secret"))

@dataclass(frozen=True)
class APIConfig:
    base_url: str = field(default_factory=lambda: os.getenv("API_BASE_URL", "https://api.axentx.com"))
    api_key: str = field(default_factory=lambda: os.getenv("API_KEY", ""))

@dataclass(frozen=True)
class RecommendationConfig:
    # Thresholds for simple rule‑based recommendations
    low_usage_threshold: float = 0.2   # 20 % of max capacity
    high_usage_threshold: float = 0.8  # 80 % of max capacity
    # Cost‑model constants
    default_cost_per_unit: float = 0.01
    # Email subject
    email_subject: str = "Axentx Cost‑Optimization Recommendations"