import asyncio
from queue import Queue

class RealTimeAIGateway:
    def __init__(self):
        self.request_queue = Queue()
        self.running_tasks = []

    async def handle_request(self, request):
        # Simulate processing an AI request
        await asyncio.sleep(0.1)  # Simulated latency
        return {"result": f"Processed {request}"}

    async def process_requests(self):
        while True:
            if not self.request_queue.empty():
                request = self.request_queue.get()
                task = asyncio.create_task(self.handle_request(request))
                self.running_tasks.append(task)
                result = await task
                print(result)
                self.running_tasks.remove(task)
            await asyncio.sleep(0.01)

    def enqueue_request(self, request):
        self.request_queue.put(request)

    def start(self):
        asyncio.run(self.process_requests())