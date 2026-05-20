from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """
    One‑to‑one extension of Django's User model.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='User'
    )
    product_type = models.CharField(
        max_length=100,
        help_text='e.g. SaaS, SaaS‑Plus, Enterprise'
    )
    mrr = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text='Monthly Recurring Revenue in USD'
    )
    mau = models.PositiveIntegerField(
        help_text='Monthly Active Users'
    )
    marketing_channels = models.CharField(
        max_length=200,
        help_text='Comma‑separated list of channels'
    )

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f'{self.user.username} – {self.product_type}'