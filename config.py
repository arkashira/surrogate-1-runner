import os
from dataclasses import dataclass

@dataclass(frozen=True)
class EmailConfig:
    sender: str = os.getenv("ALERT_EMAIL_SENDER", "alerts@axentx.com")
    smtp_host: str = os.getenv("SMTP_HOST", "smtp.example.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "465"))
    username: str = os.getenv("SMTP_USER", "alerts@axentx.com")
    password: str = os.getenv("SMTP_PASSWORD", "")          # keep secret in vault
    use_ssl: bool = True

# Global defaults – can be overridden per‑environment
DEFAULT_ALERT_THRESHOLD = float(os.getenv("DEFAULT_ALERT_THRESHOLD", "0"))  # 0 ⇒ use 10 % of balance
DAILY_ALERT_COOLDOWN = int(os.getenv("DAILY_ALERT_COOLDOWN", "1"))          # days