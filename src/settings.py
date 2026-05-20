import os
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Settings:
    # Celery
    broker_url: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    result_backend: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

    # AWS / S3
    aws_access_key_id: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region: str = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    reports_s3_bucket: str = os.getenv("REPORTS_S3_BUCKET", "surrogate-reports")
    reports_s3_prefix: str = os.getenv("REPORTS_S3_PREFIX", "daily/")

    # Misc
    report_retry_max: int = int(os.getenv("REPORT_RETRY_MAX", "3"))
    report_retry_delay: int = int(os.getenv("REPORT_RETRY_DELAY", "60"))  # seconds

settings = Settings()