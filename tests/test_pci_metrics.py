import unittest
from unittest.mock import patch
from monitoring.pci_metrics import PCIMetricsCollector

class TestPCIMetricsCollector(unittest.TestCase):
    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    def test_collect_pci_metrics(self, mock_virtual_memory, mock_cpu_percent):
        mock_cpu_percent.return_value = 50.0
        mock_virtual_memory.return_value.percent = 60.0

        collector = PCIMetricsCollector()
        collector.collect_pci_metrics()

        self.assertEqual(collector.pci_bandwidth_gauge._value.get(), 50.0)
        self.assertEqual(collector.frame_timing_gauge._value.get(), 60.0)

if __name__ == '__main__':
    unittest.main()