from pathlib import Path
from dataclasses import dataclass, field

BASE_DIR = Path(__file__).resolve().parent.parent

@dataclass
class Config:
    aws_region: str = "us-east-1"
    lookback_days: int = 30
    forecast_horizon_days: int = 30
    email_from: str = "cost-radar@company.com"
    email_to: list[str] = field(default_factory=lambda: ["ops@company.com"])
    smtp_server: str = "smtp.company.com"
    smtp_port: int = 587
    smtp_user: str = "cost-radar@company.com"
    smtp_password: str = "REPLACE_WITH_SECRET"
    db_path: Path = BASE_DIR / "cost_radar.db"
    accuracy_target: float = 0.95   # 95%
    max_variance_percent: float = 5.0  # 5%

config = Config()