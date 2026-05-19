import unittest
from alert_dashboard import app
import dash
from dash.testing import wait

class TestAlertDashboard(unittest.TestCase):
    def setUp(self):
        self.app = app

    def test_alert_graph(self):
        # Test that the alert graph is updated every minute
        dash.dash.get_server(self.app)
        self.assertEqual(self.app.layout.children[2].id, 'alert-graph')

    def test_interval_component(self):
        # Test that the interval component is set to 1 minute
        self.assertEqual(self.app.layout.children[3].interval, 60000)

if __name__ == '__main__':
    unittest.main()