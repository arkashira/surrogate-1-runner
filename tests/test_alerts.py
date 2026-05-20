import os
import unittest
from unittest.mock import patch
from config.alerts import AlertConfig

class TestAlertConfig(unittest.TestCase):
    def setUp(self):
        self.alert_config = AlertConfig()

    def test_load_config(self):
        with patch.dict(os.environ, {'SILENCED_POLICIES': 'policy1, policy2'}):
            self.alert_config.load_config()
            self.assertTrue(self.alert_config.is_policy_silenced('policy1'))
            self.assertTrue(self.alert_config.is_policy_silenced('policy2'))
            self.assertFalse(self.alert_config.is_policy_silenced('policy3'))

    def test_silence_policy(self):
        self.alert_config.silence_policy('policy1')
        self.assertTrue(self.alert_config.is_policy_silenced('policy1'))

    def test_unsilence_policy(self):
        self.alert_config.silence_policy('policy1')
        self.alert_config.unsilence_policy('policy1')
        self.assertFalse(self.alert_config.is_policy_silenced('policy1'))

if __name__ == '__main__':
    unittest.main()