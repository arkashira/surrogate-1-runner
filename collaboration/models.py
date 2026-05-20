from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Document(models.Model):
    """
    Very small model that represents a collaborative document.
    In a real project you would add title, content, ACLs, etc.
    """
    title = models.CharField(max_length=255, default="Untitled")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document {self.id}: {self.title}"


class MentionNotification(models.Model):
    """
    Stores a mention that a user received inside a document.
    """
    mentioned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mentions")
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="mentions")
    message = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mention of {self.mentioned_user} in {self.document}"