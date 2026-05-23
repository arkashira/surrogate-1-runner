from rest_framework import generics
from models.audit_log import AuditLog
from serializers.audit_log_serializer import AuditLogSerializer

class AuditLogListView(generics.ListAPIView):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        model_id = self.request.query_params.get('model_id', None)
        if model_id is not None:
            queryset = queryset.filter(model_id=model_id)
        return queryset