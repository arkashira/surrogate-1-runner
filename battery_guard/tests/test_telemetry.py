import unittest
from telemetry import Telemetry
from config import get_config

class TestTelemetry(unittest.TestCase):
    def test_track(self):
        telemetry = Telemetry()
        telemetry.track('test_command', '2023-03-01 12:00:00', 'Ubuntu 20.04')

    def test_disabled_telemetry(self):
        config = get_config()
        config.telemetry_enabled = False
        config.save()
        telemetry = Telemetry()
        telemetry.track('test_command', '2023-03-01 12:00:00', 'Ubuntu 20.04')

if __name__ == '__main__':
    unittest.main()