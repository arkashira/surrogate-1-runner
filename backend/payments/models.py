from django.db import models

class Subscription(models.Model):
    user_id = models.IntegerField()
    stripe_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user_id} - {self.stripe_id} - {self.status}"