import socket
from collections import defaultdict

class TCPStreamParser:
    def __init__(self):
        self.streams = defaultdict(list)

    def parse_packet(self, packet):
        ip_header = packet[:20]
        iph = unpack('!BBHHHBBH4s4s', ip_header)
        version_ihl = iph[0]
        ihl = version_ihl & 0xF
        iph_length = ihl * 4
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8])
        d_addr = socket.inet_ntoa(iph[9])

        if protocol == 6:  # TCP protocol
            tcp_header = packet[iph_length:iph_length+20]
            tcph = unpack('!HHLLBBHHH', tcp_header)
            source_port = tcph[0]
            dest_port = tcph[1]
            sequence = tcph[2]
            acknowledgement = tcph[3]
            doff_reserved = tcph[4]
            tcph_length = doff_reserved >> 4
            payload = packet[iph_length + tcph_length:]

            stream_key = (s_addr, d_addr, source_port, dest_port)
            self.streams[stream_key].append((sequence, payload))

            # Check if we have all packets in the stream
            if self._is_stream_complete(stream_key):
                return self._reassemble_stream(stream_key)

        return None

    def _is_stream_complete(self, stream_key):
        # Implement logic to check if all packets in the stream are received
        # This is a simplified version
        packets = self.streams[stream_key]
        if len(packets) < 2:
            return False
        # Check if the sequence numbers are consecutive
        for i in range(1, len(packets)):
            if packets[i][0] != packets[i-1][0] + len(packets[i-1][1]):
                return False
        return True

    def _reassemble_stream(self, stream_key):
        packets = self.streams[stream_key]
        packets.sort(key=lambda x: x[0])
        reassembled_data = b''.join([p[1] for p in packets])
        del self.streams[stream_key]
        return reassembled_data

class UDPParser:
    def parse_packet(self, packet):
        ip_header = packet[:20]
        iph = unpack('!BBHHHBBH4s4s', ip_header)
        version_ihl = iph[0]
        ihl = version_ihl & 0xF
        iph_length = ihl * 4
        protocol = iph[6]

        if protocol == 17:  # UDP protocol
            udp_header = packet[iph_length:iph_length+8]
            udph = unpack('!HHHH', udp_header)
            source_port = udph[0]
            dest_port = udph[1]
            length = udph[2]
            checksum = udph[3]
            payload = packet[iph_length+8:iph_length+8+length-8]
            return payload

        return None