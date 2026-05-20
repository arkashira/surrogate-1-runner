import unittest
from src.protocol_parser import TCPStreamParser, UDPParser

class TestProtocolParser(unittest.TestCase):
    def test_tcp_stream_parser(self):
        parser = TCPStreamParser()
        # Simulate TCP packets
        packet1 = b'\x45\x00\x00\x3c\x00\x00\x40\x00\x40\x06\x00\x00\xc0\xa8\x01\x01\xc0\xa8\x01\x02\x00\x50\x00\x50\x00\x00\x00\x00\x00\x00\x00\x00\x50\x12\xff\xff\x70\x12\x00\x00\x48\x65\x6c\x6c\x6f'
        packet2 = b'\x45\x00\x00\x3c\x00\x00\x40\x00\x40\x06\x00\x00\xc0\xa8\x01\x02\xc0\xa8\x01\x01\x00\x50\x00\x50\x01\x00\x00\x00\x00\x00\x00\x00\x50\x12\xff\xff\x70\x12\x00\x00\x57\x6f\x72\x6c\x64'

        # Parse packets
        result1 = parser.parse_packet(packet1)
        result2 = parser.parse_packet(packet2)

        # Check if the stream is reassembled
        self.assertIsNone(result1)
        self.assertEqual(result2, b'HelloWorld')

    def test_udp_parser(self):
        parser = UDPParser()
        # Simulate UDP packet
        packet = b'\x45\x00\x00\x28\x00\x00\x40\x00\x40\x11\x00\x00\xc0\xa8\x01\x01\xc0\xa8\x01\x02\x00\x35\x00\x35\x00\x00\x00\x00\x48\x65\x6c\x6c\x6f\x57\x6f\x72\x6c\x64'

        # Parse packet
        result = parser.parse_packet(packet)

        # Check if the payload is extracted
        self.assertEqual(result, b'HelloWorld')

if __name__ == '__main__':
    unittest.main()