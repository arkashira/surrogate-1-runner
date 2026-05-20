"""
Router for multiplexed TCP connections.

The Router uses a mapping from protocol identifiers to internal VM
addresses.  It exposes a `route` method that returns the target address
for a given protocol.  The actual socket forwarding logic is handled
elsewhere in the surrogate infrastructure.
"""

import logging
from typing import Dict, Tuple, Optional

log = logging.getLogger(__name__)

# Type alias for readability
Address = Tuple[str, int]

# Example mapping – in a real deployment this would be loaded from
# configuration or environment variables.
DEFAULT_PROTOCOL_MAP: Dict[str, Address] = {
    "https": ("10.0.0.10", 8443),
    "ssh": ("10.0.0.11", 2222),
    "rdp": ("10.0.0.12", 3389),
    "vnc": ("10.0.0.13", 5900),
}


class Router:
    """
    Router selects the internal destination for a given protocol.
    """

    def __init__(self, protocol_map: Optional[Dict[str, Address]] = None):
        """
        Parameters
        ----------
        protocol_map : dict, optional
            Mapping from protocol name to (host, port).  If None, the
            DEFAULT_PROTOCOL_MAP is used.
        """
        self.protocol_map = protocol_map or DEFAULT_PROTOCOL_MAP
        log.debug("Router initialized with mapping: %s", self.protocol_map)

    def route(self, protocol: str) -> Optional[Address]:
        """
        Return the target address for the given protocol.

        Parameters
        ----------
        protocol : str
            Protocol identifier returned by the detector.

        Returns
        -------
        tuple or None
            (host, port) tuple if the protocol is known, otherwise None.
        """
        target = self.protocol_map.get(protocol)
        if target:
            log.debug("Routing %s to %s", protocol, target)
        else:
            log.warning("No routing entry for protocol: %s", protocol)
        return target