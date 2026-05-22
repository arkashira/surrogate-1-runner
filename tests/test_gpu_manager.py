import unittest
from unittest.mock import patch
from src.gpu_manager import GPUManager

class TestGPUManager(unittest.TestCase):
    @patch('torch.cuda.is_available', return_value=True)
    @patch('torch.cuda.device_count', return_value=4)
    def test_detect_gpus(self, mock_device_count, mock_is_available):
        gpu_manager = GPUManager()
        self.assertEqual(gpu_manager.available_gpus, [0, 1, 2, 3])

    @patch('torch.cuda.is_available', return_value=True)
    @patch('torch.cuda.device_count', return_value=4)
    def test_allocate_gpu(self, mock_device_count, mock_is_available):
        gpu_manager = GPUManager()
        task_id = "task1"
        gpu_id = gpu_manager.allocate_gpu(task_id)
        self.assertEqual(gpu_id, 0)
        self.assertEqual(gpu_manager.available_gpus, [1, 2, 3])
        self.assertEqual(gpu_manager.allocated_gpus, {task_id: 0})

    @patch('torch.cuda.is_available', return_value=True)
    @patch('torch.cuda.device_count', return_value=4)
    def test_release_gpu(self, mock_device_count, mock_is_available):
        gpu_manager = GPUManager()
        task_id = "task1"
        gpu_manager.allocate_gpu(task_id)
        result = gpu_manager.release_gpu(task_id)
        self.assertTrue(result)
        self.assertEqual(gpu_manager.available_gpus, [0, 1, 2, 3])
        self.assertEqual(gpu_manager.allocated_gpus, {})

    @patch('torch.cuda.is_available', return_value=True)
    @patch('torch.cuda.device_count', return_value=4)
    def test_get_gpu_info(self, mock_device_count, mock_is_available):
        gpu_manager = GPUManager()
        task_id = "task1"
        gpu_manager.allocate_gpu(task_id)
        gpu_info = gpu_manager.get_gpu_info()
        self.assertEqual(gpu_info["available_gpus"], [1, 2, 3])
        self.assertEqual(gpu_info["allocated_gpus"], [0])

if __name__ == '__main__':
    unittest.main()