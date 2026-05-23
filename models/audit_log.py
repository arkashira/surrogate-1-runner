from django.db import models
from django.utils import timezone

class AuditLog(models.Model):
    model_id = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    rule_results = models.JSONField()
    compliance_status = models.CharField(max_length=50)

    def __str__(self):
        return f"AuditLog for model {self.model_id} at {self.timestamp}"