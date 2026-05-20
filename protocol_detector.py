"""
Protocol detection for multiplexed TCP traffic.

This module provides a simple heuristic-based detector that inspects the first
few bytes of a TCP stream and returns a protocol identifier.  It is used by
the surrogate router to decide where to forward the connection.
"""

import logging
from typing import Optional

log = logging.getLogger(__name__)

# Protocol constants
PROTOCOL_HTTPS = "https"
PROTOCOL_SSH = "ssh"
PROTOCOL_RDP = "rdp"
PROTOCOL_VNC = "vnc"
PROTOCOL_UNKNOWN = "unknown"

# Minimum number of bytes required for detection
MIN_DETECT_BYTES = 4


def detect(data: bytes) -> str:
    """
    Detect the protocol from the initial bytes of a TCP stream.

    Parameters
    ----------
    data : bytes
        The first few bytes received from the client.

    Returns
    -------
    str
        One of the protocol constants defined above.
    """
    if not data:
        return PROTOCOL_UNKNOWN

    # Ensure we have enough data for the longest detection rule
    if len(data) < MIN_DETECT_BYTES:
        # Pad with zeros to avoid index errors
        data = data.ljust(MIN_DETECT_BYTES, b"\x00")

    # HTTPS/TLS handshake: 0x16 0x03 0x01-0x03
    if data[0] == 0x16 and data[1] == 0x03 and data[2] in (0x01, 0x02, 0x03):
        log.debug("Detected HTTPS/TLS handshake")
        return PROTOCOL_HTTPS

    # SSH: starts with "SSH-"
    if data.startswith(b"SSH-"):
        log.debug("Detected SSH handshake")
        return PROTOCOL_SSH

    # RDP: T.124 initial packet starts with 0x03 0x00 0x00 0x00
    if data[0] == 0x03 and data[1] == 0x00 and data[2] == 0x00 and data[3] == 0x00:
        log.debug("Detected RDP/T.124 handshake")
        return PROTOCOL_RDP

    # VNC: starts with "RFB"
    if data.startswith(b"RFB"):
        log.debug("Detected VNC handshake")
        return PROTOCOL_VNC

    log.debug("Protocol unknown")
    return PROTOCOL_UNKNOWN