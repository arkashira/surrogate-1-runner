from django.db import models
from django.utils import timezone
import uuid

class ApprovalLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requestor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    file = models.ForeignKey('File', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
    revoked = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def is_active(self):
        return not self.is_expired() and not self.revoked and not self.used

    def __str__(self):
        return f"ApprovalLink {self.id} for {self.file}"