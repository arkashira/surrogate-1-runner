import unittest
from unittest.mock import patch, MagicMock
from axentx.surrogate.gpu import GPUDiscovry, GPUAllocation

class TestGPUDiscovry(unittest.TestCase):
    def setUp(self):
        self.gpu_discovery = GPUDiscovry()

    @patch('axentx.surrogate.gpu.subprocess')
    def test_discover_gpus(self, mock_subprocess):
        mock_subprocess.check_output.return_value = (
            b'GPU 0: NVIDIA GeForce RTX 3090 (UUID: GPU-00000000-0000-0000-0000-000000000000)\n'
            b'  Total memory: 24576 MiB\n'
            b'  PCIe bandwidth: 16 GT/s\n'
            b'  Driver version: 510.47.03\n'
            b'GPU 1: NVIDIA GeForce RTX 3090 (UUID: GPU-00000000-0000-0000-0000-000000000001)\n'
            b'  Total memory: 24576 MiB\n'
            b'  PCIe bandwidth: 16 GT/s\n'
            b'  Driver version: 510.47.03\n'
        )
        gpus = self.gpu_discovery.discover_gpus()
        self.assertEqual(len(gpus), 2)
        self.assertEqual(gpus[0]['id'], 'GPU-00000000-0000-0000-0000-000000000000')
        self.assertEqual(gpus[0]['total_memory'], 24576)
        self.assertEqual(gpus[0]['pcie_bandwidth'], 16)
        self.assertEqual(gpus[0]['driver_version'], '510.47.03')

    @patch('axentx.surrogate.gpu.subprocess')
    def test_discover_gpus_no_gpus(self, mock_subprocess):
        mock_subprocess.check_output.return_value = b'No GPUs found'
        gpus = self.gpu_discovery.discover_gpus()
        self.assertEqual(len(gpus), 0)

class TestGPUAllocation(unittest.TestCase):
    def setUp(self):
        self.gpu_allocation = GPUAllocation()

    def test_allocate_gpu(self):
        gpu_id = 'GPU-00000000-0000-0000-0000-000000000000'
        handle = self.gpu_allocation.allocate_gpu(gpu_id)
        self.assertIsNotNone(handle)
        self.assertEqual(self.gpu_allocation.allocate_gpu(gpu_id), None)

    def test_allocate_gpu_invalid_id(self):
        gpu_id = 'invalid_id'
        handle = self.gpu_allocation.allocate_gpu(gpu_id)
        self.assertIsNone(handle)

    def test_release_gpu(self):
        gpu_id = 'GPU-00000000-0000-0000-0000-000000000000'
        handle = self.gpu_allocation.allocate_gpu(gpu_id)
        self.gpu_allocation.release_gpu(handle)
        new_handle = self.gpu_allocation.allocate_gpu(gpu_id)
        self.assertIsNotNone(new_handle)
        self.assertNotEqual(handle, new_handle)

if __name__ == '__main__':
    unittest.main()