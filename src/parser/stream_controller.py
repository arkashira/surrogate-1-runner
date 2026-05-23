import asyncio
from typing import Callable

class StreamController:
    def __init__(self, buffer_size: int = 100, back_pressure_hook: Callable = None):
        self.buffer = []
        self.buffer_size = buffer_size
        self.back_pressure_hook = back_pressure_hook
        self.consumer_ready = asyncio.Event()
        self.consumer_ready.set()
        self.pipeline_saturated = False

    async def read(self, data):
        await self.consumer_ready.wait()
        if self.pipeline_saturated:
            await self.back_pressure_hook()
            return
        if len(self.buffer) >= self.buffer_size:
            self.pipeline_saturated = True
            await self.back_pressure_hook()
            self.consumer_ready.clear()
        self.buffer.append(data)
        if len(self.buffer) < self.buffer_size:
            self.pipeline_saturated = False
            self.consumer_ready.set()

    async def process(self):
        while True:
            if self.buffer:
                item = self.buffer.pop(0)
                # Simulate processing time
                await asyncio.sleep(0.1)
                print(f"Processed: {item}")
                if not self.buffer:
                    self.consumer_ready.set()
            else:
                await asyncio.sleep(0.1)

# Test cases
async def test_stream_controller():
    controller = StreamController(buffer_size=3, back_pressure_hook=back_pressure_hook)
    tasks = [
        asyncio.create_task(controller.read(i)) for i in range(5)
    ]
    await asyncio.gather(*tasks)
    await controller.process()

async def back_pressure_hook():
    print("Back-pressure signal received")

if __name__ == "__main__":
    asyncio.run(test_stream_controller())