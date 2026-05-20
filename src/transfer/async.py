import asyncio
import logging
from typing import Any, Awaitable

logger = logging.getLogger(__name__)

class AsyncTransferWrapper:
    def __init__(self, nvlink_available: bool):
        self.nvlink_available = nvlink_available

    async def transfer_tensor(self, tensor: Any, src_gpu: int, dst_gpu: int) -> Awaitable:
        if self.nvlink_available:
            logger.info("Using NVLink for tensor transfer.")
            return await self._nvlink_transfer(tensor, src_gpu, dst_gpu)
        else:
            logger.warning("NVLink not available, falling back to PCIe.")
            return await self._pcie_transfer(tensor, src_gpu, dst_gpu)

    async def _nvlink_transfer(self, tensor: Any, src_gpu: int, dst_gpu: int) -> Awaitable:
        # Simulate NVLink transfer
        await asyncio.sleep(0.000005)  # Simulating 5 µs latency
        return tensor

    async def _pcie_transfer(self, tensor: Any, src_gpu: int, dst_gpu: int) -> Awaitable:
        # Simulate PCIe transfer
        await asyncio.sleep(0.00001)  # Simulating slightly higher latency than NVLink
        return tensor

# Example usage
async def main():
    wrapper = AsyncTransferWrapper(nvlink_available=True)
    tensor = "example_tensor"
    result = await wrapper.transfer_tensor(tensor, 0, 1)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())