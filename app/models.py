from decimal import Decimal
from django.db import models


class Cost(models.Model):
    """
    One row = the amount a *worker* spent on a *provider*.
    """
    worker_id = models.CharField(max_length=64)          # e.g. “worker‑42”
    provider   = models.CharField(max_length=64)        # e.g. “aws”, “gcp”
    amount     = models.DecimalField(max_digits=20,
                                     decimal_places=2,
                                     default=Decimal("0.00"))

    class Meta:
        indexes = [
            models.Index(fields=["worker_id"]),
            models.Index(fields=["provider"]),
        ]

    def __str__(self) -> str:
        return f"{self.worker_id} – {self.provider}: {self.amount}"