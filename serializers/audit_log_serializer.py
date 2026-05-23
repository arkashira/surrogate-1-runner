from rest_framework import serializers
from models.audit_log import AuditLog

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ['model_id', 'timestamp', 'rule_results', 'compliance_status']