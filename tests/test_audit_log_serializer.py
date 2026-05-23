from django.test import TestCase
from models.audit_log import AuditLog
from serializers.audit_log_serializer import AuditLogSerializer

class AuditLogSerializerTest(TestCase):
    def setUp(self):
        self.audit_log = AuditLog.objects.create(
            model_id='test_model',
            rule_results={'rule1': 'pass', 'rule2': 'fail'},
            compliance_status='non-compliant'
        )
        self.serializer = AuditLogSerializer(instance=self.audit_log)

    def test_serializer_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['model_id', 'timestamp', 'rule_results', 'compliance_status']))