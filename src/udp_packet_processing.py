import socket
import struct
from typing import Tuple, Optional

class UDPPacketProcessor:
    def __init__(self):
        self.game_traffic_handlers = {}

    def register_game_handler(self, game_id: str, handler):
        """Register a handler for specific game traffic."""
        self.game_traffic_handlers[game_id] = handler

    def process_packet(self, packet: bytes, source_addr: Tuple[str, int]) -> Optional[bytes]:
        """
        Process a UDP packet and determine if it's game traffic.
        Returns the processed packet if it's game traffic, None otherwise.
        """
        # Basic packet structure: [header][payload]
        # For game traffic, we expect a specific header format
        if len(packet) < 8:
            return None

        # Extract game ID from the packet header
        game_id = packet[4:8].hex()

        if game_id in self.game_traffic_handlers:
            return self.game_traffic_handlers[game_id](packet, source_addr)
        return None