import unittest
import os
import json
from datetime import datetime, timedelta
from src.cost_alerts import CostAlert

class TestCostAlert(unittest.TestCase):
    def setUp(self):
        self.test_config_path = "config/test_cost_alerts.json"
        self.cost_alert = CostAlert(self.test_config_path)
        self.test_data = {
            "thresholds": {
                "service1": 100.0,
                "service2": 200.0
            },
            "alerts": []
        }
        with open(self.test_config_path, 'w') as f:
            json.dump(self.test_data, f)

    def tearDown(self):
        if os.path.exists(self.test_config_path):
            os.remove(self.test_config_path)

    def test_set_threshold(self):
        self.cost_alert.set_threshold("service3", 300.0)
        with open(self.test_config_path, 'r') as f:
            config = json.load(f)
        self.assertEqual(config["thresholds"]["service3"], 300.0)

    def test_check_costs(self):
        current_costs = {
            "service1": 150.0,
            "service2": 250.0
        }
        alerts = self.cost_alert.check_costs(current_costs)
        self.assertEqual(len(alerts), 2)
        self.assertEqual(alerts[0]["service"], "service1")
        self.assertEqual(alerts[1]["service"], "service2")

    def test_get_alerts(self):
        test_alerts = [
            {"service": "service1", "cost": 150.0, "threshold": 100.0, "timestamp": (datetime.now() - timedelta(hours=1)).isoformat()},
            {"service": "service2", "cost": 250.0, "threshold": 200.0, "timestamp": datetime.now().isoformat()}
        ]
        self.test_data["alerts"] = test_alerts
        with open(self.test_config_path, 'w') as f:
            json.dump(self.test_data, f)

        alerts = self.cost_alert.get_alerts()
        self.assertEqual(len(alerts), 2)

        alerts = self.cost_alert.get_alerts(hours=1)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["service"], "service2")

if __name__ == '__main__':
    unittest.main()