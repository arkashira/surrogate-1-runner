import os
from dataclasses import dataclass

@dataclass
class Config:
    """Centralized configuration management."""
    
    # Database
    DATABASE_URL: str = os.environ.get('DATABASE_URL', 'sqlite:///deals.db')
    
    # Email
    MAIL_SERVER: str = os.environ.get('MAIL_SERVER', 'smtp.example.com')
    MAIL_PORT: int = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS: bool = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME: str = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD: str = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER: str = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # App
    DEBUG: bool = os.environ.get('DEBUG', 'false').lower() == 'true'

config = Config()