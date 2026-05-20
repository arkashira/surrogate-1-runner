from django.db import models

class Alert(models.Model):
    """
    Represents an alert message.
    
    Attributes:
        message (str): The alert message.
        created_at (datetime): The timestamp when the alert was created.
    """
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message