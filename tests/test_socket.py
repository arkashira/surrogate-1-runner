import unittest
import websockets
from axentx import settings

class TestSocket(unittest.TestCase):
    async def test_handle_connection(self):
        async with websockets.connect(f'ws://{settings.WEB_SOCKET_HOST}:{settings.WEB_SOCKET_PORT}') as websocket:
            await websocket.send('ping')
            response = await websocket.recv()
            self.assertEqual(response, 'pong')

if __name__ == '__main__':
    unittest.main()