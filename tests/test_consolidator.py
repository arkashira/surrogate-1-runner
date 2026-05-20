import unittest
from services.consolidator import AlertConsolidator, Alert
import time

class TestAlertConsolidator(unittest.TestCase):
    def test_consolidate_alerts(self):
        consolidator = AlertConsolidator(window_size=300)
        alert1 = Alert("service1", "error1", int(time.time()))
        alert2 = Alert("service1", "error1", int(time.time()) - 100)
        consolidator.ingest_alert(alert1)
        consolidator.ingest_alert(alert2)
        consolidated = consolidator.consolidate()
        self.assertEqual(len(consolidated), 1)
        self.assertEqual(consolidated[0]["count"], 2)

    def test_alerts_outside_window(self):
        consolidator = AlertConsolidator(window_size=300)
        alert1 = Alert("service1", "error1", int(time.time()))
        alert2 = Alert("service1", "error1", int(time.time()) - 400)
        consolidator.ingest_alert(alert1)
        consolidator.ingest_alert(alert2)
        consolidated = consolidator.consolidate()
        self.assertEqual(len(consolidated), 1)
        self.assertEqual(consolidated[0]["count"], 1)

if __name__ == "__main__":
    unittest.main()