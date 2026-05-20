from django.db import models

class AuditLog(models.Model):
    """Immutable log of every important action (registration, delivery, failure)."""
    ACTION_CHOICES = [
        ('WEBHOOK_REGISTERED', 'Webhook Registered'),
        ('WEBHOOK_DELIVERED', 'Webhook Delivered'),
        ('WEBHOOK_DELIVERY_FAILED', 'Webhook Delivery Failed'),
    ]

    action = models.CharField(max_length=32, choices=ACTION_CHOICES)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.get_action_display()} @ {self.created_at.isoformat()}"