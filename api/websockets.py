import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AgentStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        asyncio.create_task(self.send_agent_status())

    async def disconnect(self, close_code):
        pass

    async def send_agent_status(self):
        while True:
            # Simulate fetching real-time agent health data
            agent_health_data = {
                'agents': [
                    {'id': 1, 'status': 'healthy', 'latency': 0.1},
                    {'id': 2, 'status': 'degraded', 'latency': 0.5},
                    # Add more agents as needed
                ]
            }
            await self.send(json.dumps(agent_health_data))
            await asyncio.sleep(0.1)  # Refresh rate <1s

    async def receive(self, text_data):
        pass

class WorkflowMetricsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        asyncio.create_task(self.send_workflow_metrics())

    async def disconnect(self, close_code):
        pass

    async def send_workflow_metrics(self):
        while True:
            # Simulate fetching real-time workflow metrics data
            workflow_metrics_data = {
                'workflows': [
                    {'id': 1, 'execution_time': 2.3, 'latency_heatmap': [0.1, 0.2, 0.3]},
                    {'id': 2, 'execution_time': 4.5, 'latency_heatmap': [0.4, 0.5, 0.6]},
                    # Add more workflows as needed
                ]
            }
            await self.send(json.dumps(workflow_metrics_data))
            await asyncio.sleep(0.1)  # Refresh rate <1s

    async def receive(self, text_data):
        pass