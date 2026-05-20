import socket
from protocol_parser import TCPStreamParser, UDPParser

class Multiplexer:
    def __init__(self):
        self.tcp_parser = TCPStreamParser()
        self.udp_parser = UDPParser()

    def handle_packet(self, packet):
        # Determine protocol and handle accordingly
        ip_header = packet[:20]
        iph = unpack('!BBHHHBBH4s4s', ip_header)
        protocol = iph[6]

        if protocol == 6:  # TCP
            result = self.tcp_parser.parse_packet(packet)
            if result:
                self.forward_tcp_stream(result)
        elif protocol == 17:  # UDP
            result = self.udp_parser.parse_packet(packet)
            if result:
                self.forward_udp_datagram(result)

    def forward_tcp_stream(self, stream):
        # Implement logic to forward the TCP stream
        print(f"Forwarding TCP stream: {stream}")

    def forward_udp_datagram(self, datagram):
        # Implement logic to forward the UDP datagram
        print(f"Forwarding UDP datagram: {datagram}")

# Example usage
if __name__ == '__main__':
    multiplexer = Multiplexer()
    # Simulate incoming packets
    tcp_packet = b'\x45\x00\x00\x3c\x00\x00\x40\x00\x40\x06\x00\x00\xc0\xa8\x01\x01\xc0\xa8\x01\x02\x00\x50\x00\x50\x00\x00\x00\x00\x00\x00\x00\x00\x50\x12\xff\xff\x70\x12\x00\x00\x48\x65\x6c\x6c\x6f'
    udp_packet = b'\x45\x00\x00\x28\x00\x00\x40\x00\x40\x11\x00\x00\xc0\xa8\x01\x01\xc0\xa8\x01\x02\x00\x35\x00\x35\x00\x00\x00\x00\x48\x65\x6c\x6c\x6f\x57\x6f\x72\x6c\x64'

    multiplexer.handle_packet(tcp_packet)
    multiplexer.handle_packet(udp_packet)