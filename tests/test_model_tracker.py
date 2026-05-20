import unittest
from monitoring.model_tracker import ModelTracker

class TestModelTracker(unittest.TestCase):
    def setUp(self):
        self.config_path = '/tmp/test_config.json'
        self.tracker = ModelTracker(self.config_path)
        self.new_config = {'model_version': 'v2.0'}

    def test_track_model_version_no_violation(self):
        self.tracker.current_config = {'model_version': 'v2.0'}
        result = self.tracker.track_model_version(self.new_config)
        self.assertTrue(result)

    def test_track_model_version_with_violation(self):
        self.tracker.current_config = {'model_version': 'v1.0'}
        result = self.tracker.track_model_version(self.new_config)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()