from django.test import TestCase
from .models import Alert

class AlertTest(TestCase):
    def test_alert_creation(self):
        """
        Tests the creation of an alert.
        
        Verifies that the alert message is correctly stored in the database.
        """
        alert = Alert.objects.create(message='Test Alert')
        self.assertEqual(alert.message, 'Test Alert')