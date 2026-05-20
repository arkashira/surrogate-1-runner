import unittest
from update_manager import UpdateManager

class TestUpdateManager(unittest.TestCase):
    def setUp(self):
        self.updater = UpdateManager("v1.0.0")

    def test_check_for_updates(self):
        latest_version = self.updater.check_for_updates()
        self.assertIsNotNone(latest_version)

    def test_download_update(self):
        latest_version = self.updater.check_for_updates()
        if latest_version:
            filename = self.updater.download_update(latest_version)
            self.assertTrue(os.path.exists(filename))

    def test_apply_update(self):
        latest_version = self.updater.check_for_updates()
        if latest_version:
            filename = self.updater.download_update(latest_version)
            if filename:
                self.updater.apply_update(filename)
                self.assertTrue(os.path.exists("/opt/axentx/surrogate-1/update_manager.py"))

if __name__ == "__main__":
    unittest.main()