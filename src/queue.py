from asyncio import Queue

class RequestQueue(Queue):
    def __init__(self):
        super().__init__()

    def enqueue(self, item):
        self.put_nowait(item)

    async def dequeue(self):
        return await self.get()