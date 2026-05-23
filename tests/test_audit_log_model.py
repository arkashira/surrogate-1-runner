from django.test import TestCase
from models.audit_log import AuditLog

class AuditLogModelTest(TestCase):
    def setUp(self):
        self.audit_log = AuditLog.objects.create(
            model_id='test_model',
            rule_results={'rule1': 'pass', 'rule2': 'fail'},
            compliance_status='non-compliant'
        )

    def test_audit_log_creation(self):
        self.assertEqual(self.audit_log.model_id, 'test_model')
        self.assertEqual(self.audit_log.rule_results, {'rule1': 'pass', 'rule2': 'fail'})
        self.assertEqual(self.audit_log.compliance_status, 'non-compliant')