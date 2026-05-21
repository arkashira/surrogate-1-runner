import unittest
from unittest.mock import patch
from src.gpu_discovery import GPUDiscovery

class TestGPUDiscovery(unittest.TestCase):
    @patch('subprocess.run')
    def test_detect_gpus(self, mock_run):
        # Mock the subprocess.run output
        mock_run.return_value.stdout = """
00:02.0 VGA compatible controller [0300]: Intel Corporation Device [8086:1234] (rev 02)
    Subsystem: Intel Corporation Device [8086:5678]
    Kernel driver in use: i915
    Kernel modules: i915
01:00.0 VGA compatible controller [0300]: NVIDIA Corporation Device [10de:2345] (rev a1)
    Subsystem: NVIDIA Corporation Device [10de:6789]
    Kernel driver in use: nvidia
    Kernel modules: nvidia
"""

        gpu_discovery = GPUDiscovery()
        gpus = gpu_discovery.detect_gpus()

        self.assertEqual(len(gpus), 2)
        self.assertEqual(gpus[0]['driver'], 'i915')
        self.assertEqual(gpus[1]['driver'], 'nvidia')

    def test_generate_load_balancing_profile(self):
        gpu_discovery = GPUDiscovery()
        gpu_discovery.gpu_info = [{'driver': 'i915'}, {'driver': 'nvidia'}]

        profile = gpu_discovery.generate_load_balancing_profile()

        self.assertEqual(profile['gpu_count'], 2)
        self.assertEqual(profile['load_balancing'], 'round_robin')
        self.assertTrue(profile['performance_overlay'])

if __name__ == '__main__':
    unittest.main()