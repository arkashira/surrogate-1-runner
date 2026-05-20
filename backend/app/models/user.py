from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    email_notifications = models.BooleanField(default=True)

    def __str__(self):
        return self.email