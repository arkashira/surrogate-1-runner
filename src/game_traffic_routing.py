from typing import Tuple, Dict, Callable
import socket

class GameTrafficRouter:
    def __init__(self):
        self.routing_rules = {}
        self.sockets: Dict[str, socket.socket] = {}

    def add_routing_rule(self, game_id: str, destination: Tuple[str, int]):
        """Add a routing rule for a specific game."""
        self.routing_rules[game_id] = destination

    def create_socket(self, game_id: str):
        """Create a socket for a specific game if it doesn't exist."""
        if game_id not in self.sockets:
            self.sockets[game_id] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def route_packet(self, game_id: str, packet: bytes, source_addr: Tuple[str, int]) -> bool:
        """
        Route a game packet to its destination.
        Returns True if routing was successful, False otherwise.
        """
        if game_id not in self.routing_rules:
            return False

        destination = self.routing_rules[game_id]
        self.create_socket(game_id)

        try:
            self.sockets[game_id].sendto(packet, destination)
            return True
        except Exception as e:
            print(f"Error routing packet for game {game_id}: {e}")
            return False