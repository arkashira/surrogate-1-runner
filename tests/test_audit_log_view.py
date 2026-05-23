from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from models.audit_log import AuditLog

class AuditLogViewTest(APITestCase):
    def setUp(self):
        self.audit_log1 = AuditLog.objects.create(
            model_id='model1',
            rule_results={'rule1': 'pass'},
            compliance_status='compliant'
        )
        self.audit_log2 = AuditLog.objects.create(
            model_id='model2',
            rule_results={'rule1': 'fail'},
            compliance_status='non-compliant'
        )
        self.url = reverse('audit-log-list')

    def test_get_all_audit_logs(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_audit_logs_by_model_id(self):
        response = self.client.get(self.url, {'model_id': 'model1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['model_id'], 'model1')