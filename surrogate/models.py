from django.db import models

class FounderProfile(models.Model):
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    stage = models.CharField(max_length=50, blank=True, null=True)
    target_market = models.CharField(max_length=100, blank=True, null=True)
    pricing_model = models.CharField(max_length=50, blank=True, null=True)
    current_funnel = models.CharField(max_length=100, blank=True, null=True)
    biggest_growth_pain = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email