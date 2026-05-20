"""
Unit tests for the protocol detection logic.
"""

import pytest
from surrogate_1.protocol_detector import (
    detect,
    PROTOCOL_HTTPS,
    PROTOCOL_SSH,
    PROTOCOL_RDP,
    PROTOCOL_VNC,
    PROTOCOL_UNKNOWN,
)


@pytest.mark.parametrize(
    "data,expected",
    [
        (b"\x16\x03\x01\x02", PROTOCOL_HTTPS),
        (b"SSH-2.0-OpenSSH_8.4", PROTOCOL_SSH),
        (b"\x03\x00\x00\x00", PROTOCOL_RDP),
        (b"RFB 003.008", PROTOCOL_VNC),
        (b"", PROTOCOL_UNKNOWN),
        (b"\x00\x01\x02\x03", PROTOCOL_UNKNOWN),
    ],
)
def test_detect_protocol(data, expected):
    assert detect(data) == expected