import unittest
from unittest.mock import patch, MagicMock
from protocol_handlers.udp_handler import UDPMultiplexer

class TestUDPMultiplexer(unittest.TestCase):
    @patch('socket.socket')
    def test_handle_packet_known_client(self, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        multiplexer = UDPMultiplexer('127.0.0.1', 12345)
        multiplexer.clients = {('192.168.1.1', 5678): ('10.0.0.1', 8080)}
        
        multiplexer.handle_packet(b'test_packet', ('192.168.1.1', 5678))
        
        mock_socket_instance.sendto.assert_called_once_with(b'test_packet', ('10.0.0.1', 8080))

    @patch('socket.socket')
    def test_handle_packet_unknown_client(self, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        multiplexer = UDPMultiplexer('127.0.0.1', 12345)
        
        multiplexer.handle_packet(b'test_packet', ('192.168.1.2', 5678))
        
        mock_socket_instance.sendto.assert_not_called()

if __name__ == '__main__':
    unittest.main()