import asyncio
import unittest
from unittest.mock import patch
from src.transfer.async import AsyncTransferWrapper

class TestAsyncTransfer(unittest.TestCase):
    @patch('src.transfer.async.logger')
    async def test_nvlink_transfer(self, mock_logger):
        wrapper = AsyncTransferWrapper(nvlink_available=True)
        tensor = "example_tensor"
        result = await wrapper.transfer_tensor(tensor, 0, 1)
        self.assertEqual(result, tensor)
        mock_logger.info.assert_called_with("Using NVLink for tensor transfer.")

    @patch('src.transfer.async.logger')
    async def test_pcie_fallback(self, mock_logger):
        wrapper = AsyncTransferWrapper(nvlink_available=False)
        tensor = "example_tensor"
        result = await wrapper.transfer_tensor(tensor, 0, 1)
        self.assertEqual(result, tensor)
        mock_logger.warning.assert_called_with("NVLink not available, falling back to PCIe.")

if __name__ == '__main__':
    unittest.main()