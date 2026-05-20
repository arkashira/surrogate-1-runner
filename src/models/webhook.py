from django.db import models
from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator

class Webhook(models.Model):
    """A registered endpoint that will receive credit‑usage notifications."""
    url = models.URLField(
        validators=[URLValidator()],
        help_text="Target URL that must accept a JSON POST."
    )
    threshold = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Optional trigger threshold (0‑1)."
    )
    account_id = models.CharField(
        max_length=255,
        help_text="External identifier of the account that owns the webhook."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('url', 'account_id')
        indexes = [
            models.Index(fields=['account_id']),
        ]

    def __str__(self) -> str:
        return f"{self.account_id} → {self.url}"