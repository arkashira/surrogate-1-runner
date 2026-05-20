import unittest
from unittest.mock import Mock
from src.ui.multi_gpu_bridge import MultiGPUBridgeUI

class TestMultiGPUBridgeUI(unittest.TestCase):
    def setUp(self):
        self.root = Mock()
        self.app = MultiGPUBridgeUI(self.root)

    def test_configure_gpus(self):
        self.app.configure_gpus()
        self.assertTrue(self.app.configure_gpus_window.winfo_exists())

    def test_monitor_performance(self):
        self.app.monitor_performance()
        self.assertTrue(self.app.monitor_performance_window.winfo_exists())

    def test_add_gpu(self):
        self.app.add_gpu()
        self.assertEqual(self.app.gpu_listbox.get("end-1c"), "GPU 1")

    def test_remove_gpu(self):
        self.app.gpu_listbox.insert("end", "GPU 1")
        self.app.remove_gpu()
        self.assertEqual(self.app.gpu_listbox.get("end-1c"), "")

if __name__ == "__main__":
    unittest.main()