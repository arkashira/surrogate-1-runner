import unittest
from analysis.memory_usage import MemoryUsageAnalyzer

class TestMemoryUsage(unittest.TestCase):
    def setUp(self):
        self.analyzer = MemoryUsageAnalyzer()

    def test_start_stop_tracing(self):
        self.assertFalse(self.analyzer.tracemalloc_enabled)
        self.analyzer.start_tracing()
        self.assertTrue(self.analyzer.tracemalloc_enabled)
        self.analyzer.stop_tracing()
        self.assertFalse(self.analyzer.tracemalloc_enabled)

    def test_get_process_memory(self):
        memory_usage = self.analyzer.get_process_memory()
        self.assertGreater(memory_usage, 0)

    def test_monitor_memory(self):
        try:
            self.analyzer.monitor_memory(interval=0.1)
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    unittest.main()