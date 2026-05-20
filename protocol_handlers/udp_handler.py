import socket
from threading import Thread
from typing import Dict, Tuple

class UDPMultiplexer:
    def __init__(self, external_ip: str, external_port: int):
        self.external_ip = external_ip
        self.external_port = external_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((external_ip, external_port))
        self.clients: Dict[Tuple[str, int], Tuple[str, int]] = {}

    def handle_packet(self, packet: bytes, addr: Tuple[str, int]):
        if addr in self.clients:
            internal_addr = self.clients[addr]
            internal_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            internal_socket.sendto(packet, internal_addr)
            internal_socket.close()
        else:
            print(f"Unknown client {addr}. Packet dropped.")

    def start(self):
        while True:
            packet, addr = self.socket.recvfrom(65535)
            Thread(target=self.handle_packet, args=(packet, addr)).start()

def main():
    multiplexer = UDPMultiplexer('YOUR_EXTERNAL_IP', 12345)
    multiplexer.start()

if __name__ == "__main__":
    main()