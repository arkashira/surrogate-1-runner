import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from db.models import ApprovalLink

class ApprovalLinkConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send_approval_links()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass

    @database_sync_to_async
    def get_approval_links(self):
        approval_links = ApprovalLink.objects.all()
        return [{
            'id': str(link.id),
            'requestor': link.requestor.username,
            'file': link.file.name,
            'status': 'active' if link.is_active() else
                     'used' if link.used else
                     'expired' if link.is_expired() else
                     'revoked',
            'created_at': link.created_at.isoformat(),
            'expires_at': link.expires_at.isoformat()
        } for link in approval_links]

    async def send_approval_links(self):
        approval_links = await self.get_approval_links()
        await self.send(text_data=json.dumps(approval_links))