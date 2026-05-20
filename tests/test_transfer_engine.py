import unittest
from src.transfer.engine import TransferEngine
import torch

class TestTransferEngine(unittest.TestCase):
    def setUp(self):
        self.device_ids = [0, 1]
        self.engine = TransferEngine(self.device_ids)

    def test_transfer_tensor(self):
        tensor = torch.randn(1024).cuda()
        future = self.engine.transfer_tensor(tensor, 1)
        result = future.result()
        self.assertEqual(result.device.index, 1)

    def test_validate_transfer(self):
        self.engine.validate_transfer()

if __name__ == '__main__':
    unittest.main()