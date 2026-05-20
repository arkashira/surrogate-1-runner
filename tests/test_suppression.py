import unittest
from src.alert_processing.suppression import AlertSuppression

class TestAlertSuppression(unittest.TestCase):
    def setUp(self):
        self.threshold_rules = {
            'service1': 3,
            'service2': 5,
        }
        self.alerts = [
            {'service_name': 'service1', 'namespace': 'ns1', 'timestamp': 1623456789},
            {'service_name': 'service1', 'namespace': 'ns1', 'timestamp': 1623456790},
            {'service_name': 'service2', 'namespace': 'ns2', 'timestamp': 1623456791},
            # ... more alerts ...
        ]
        self.suppression = AlertSuppression(self.threshold_rules)

    def test_cluster_alerts(self):
        clusters = self.suppression.cluster_alerts(self.alerts)
        self.assertIn('service1/ns1', clusters)
        self.assertIn('service2/ns2', clusters)

    def test_suppress_alerts(self):
        self.suppression.cluster_alerts(self.alerts)
        suppressed = self.suppression.suppress_alerts()
        self.assertEqual(len(suppressed['service1/ns1'][0]), 2)  # Top 2 alerts for service1
        self.assertEqual(suppressed['service1/ns1'][1], 1)  # 1 alert suppressed for service1

if __name__ == '__main__':
    unittest.main()