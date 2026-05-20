from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from src.models.audit_log import AuditLog
from src.serializers.webhook_serializer import WebhookSerializer

class WebhookView(APIView):
    """
    POST /api/v1/credits/webhook
    Registers a new webhook for an account.
    """
    def post(self, request):
        serializer = WebhookSerializer(data=request.data)
        if serializer.is_valid():
            webhook = serializer.save()                     # persists the model
            AuditLog.objects.create(
                action='WEBHOOK_REGISTERED',
                details=f"Webhook {webhook.url} registered for account {webhook.account_id}"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Validation errors – no audit entry (they are client‑side mistakes)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)