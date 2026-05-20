import asyncio
import unittest
from unittest.mock import patch
from src.websockets import WebSocketServer

class TestWebSocketServer(unittest.TestCase):
    @patch('websockets.serve')
    def test_start(self, mock_serve):
        server = WebSocketServer('localhost', 8765)
        server.start()
        mock_serve.assert_called_once()

    @patch('asyncio.wait')
    async def test_broadcast(self, mock_wait):
        server = WebSocketServer('localhost', 8765)
        mock_clients = [asyncio.Future(), asyncio.Future()]
        server.clients = {id(client): client for client in mock_clients}
        await server.broadcast("test message")
        mock_wait.assert_called_once()

if __name__ == '__main__':
    unittest.main()