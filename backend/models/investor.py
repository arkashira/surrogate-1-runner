from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator
from django.contrib.postgres.fields import JSONField

class Investor(models.Model):
    """
    Represents a venture‑capital or private‑equity investor.

    All fields are required except the optional two‑factor secret.
    """
    email = models.EmailField(
        unique=True,
        max_length=254,
        db_index=True,
        help_text="Unique e‑mail address used for login."
    )
    password = models.CharField(
        max_length=128,
        validators=[MinLengthValidator(8)],
        help_text="Hashed password – never store plain text."
    )
    two_factor_secret = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        help_text="Secret used for TOTP 2FA (optional)."
    )

    firm_name = models.CharField(
        max_length=200,
        db_index=True,
        help_text="Name of the investment firm."
    )

    # Investment stage – keep the list short enough for a lookup table but
    # still expressive enough for most use‑cases.
    INVESTMENT_STAGE_CHOICES = [
        ('seed', 'Seed'),
        ('series_a', 'Series A'),
        ('series_b', 'Series B'),
        ('series_c', 'Series C'),
        ('series_d', 'Series D'),
        ('series_e', 'Series E'),
        ('late_stage', 'Late Stage'),
        ('growth', 'Growth'),
        ('venture', 'Venture'),
        ('private_equity', 'Private Equity'),
        ('angel', 'Angel'),
        ('corporate', 'Corporate'),
        ('other', 'Other'),
    ]
    investment_stage = models.CharField(
        max_length=20,
        choices=INVESTMENT_STAGE_CHOICES,
        db_index=True,
        help_text="Typical investment stage the firm targets."
    )

    ticket_size = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        db_index=True,
        help_text="Typical minimum investment amount (USD)."
    )

    # JSONField is stored as PostgreSQL JSONB – great for arrays of strings.
    focus_areas = JSONField(
        default=list,
        blank=True,
        help_text="List of industry focus areas (e.g. ['Technology', 'Healthcare'])."
    )
    geographic_preference = JSONField(
        default=list,
        blank=True,
        help_text="List of preferred geographies (e.g. ['North America', 'Europe'])."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['firm_name']),
            models.Index(fields=['investment_stage']),
            models.Index(fields=['ticket_size']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.firm_name} ({self.email})"

    def __repr__(self):
        return (
            f"Investor(email={self.email!r}, firm_name={self.firm_name!r}, "
            f"investment_stage={self.investment_stage!r})"
        )