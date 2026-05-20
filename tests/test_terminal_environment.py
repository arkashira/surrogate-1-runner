import asyncio
import unittest
from unittest.mock import patch
from src.terminal_environment import TerminalEnvironment

class TestTerminalEnvironment(unittest.TestCase):
    @patch('src.websockets.WebSocketServer.start')
    def test_start(self, mock_start):
        env = TerminalEnvironment('localhost', 8765)
        env.start()
        mock_start.assert_called_once()

    @patch('src.websockets.WebSocketServer.broadcast')
    async def test_add_user(self, mock_broadcast):
        env = TerminalEnvironment('localhost', 8765)
        await env.add_user("user1")
        mock_broadcast.assert_called_once()

    @patch('src.websockets.WebSocketServer.broadcast')
    async def test_remove_user(self, mock_broadcast):
        env = TerminalEnvironment('localhost', 8765)
        await env.add_user("user1")
        await env.remove_user("user1")
        self.assertEqual(len(env.users), 0)
        self.assertEqual(mock_broadcast.call_count, 2)

if __name__ == '__main__':
    unittest.main()