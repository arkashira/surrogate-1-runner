from django.db import models

class AlertLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    resource_id = models.CharField(max_length=255)
    rule_name = models.CharField(max_length=255)
    delivery_status = models.IntegerField()

    def save(self, *args, **kwargs):
        super(AlertLog, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.resource_id} - {self.rule_name} - {self.delivery_status}"