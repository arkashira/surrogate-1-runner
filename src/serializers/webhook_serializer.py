from rest_framework import serializers
from src.models.webhook import Webhook

class WebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webhook
        fields = ['url', 'threshold', 'account_id']
        extra_kwargs = {
            'url': {'required': True},
            'threshold': {'required': True, 'min_value': 0.0, 'max_value': 1.0},
            'account_id': {'required': True},
        }