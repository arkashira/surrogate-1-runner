from django.db import models

class UsageLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    token_count = models.IntegerField()
    response_time = models.FloatField()
    model_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"UsageLog({self.model_name})"

class PerformanceMetric(models.Model):
    model_name = models.CharField(max_length=100)
    accuracy = models.FloatField()
    response_time = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"PerformanceMetric({self.model_name})"