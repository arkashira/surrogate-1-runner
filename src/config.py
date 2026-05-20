"""Configuration for the Audit Impact Scoring API."""

import os
from dataclasses import dataclass


@dataclass
class Config:
    """Application configuration."""
    
    # Scoring weights (must sum to 10 for clean 0-100 scale)
    SEVERITY_WEIGHT: int = 5   # 50%
    RESOURCES_WEIGHT: int = 3  # 30%
    BUSINESS_WEIGHT: int = 2   # 20%
    
    # Input bounds
    MAX_INPUT_VALUE: int = 10
    MIN_INPUT_VALUE: int = 0
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8080"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"


config = Config()