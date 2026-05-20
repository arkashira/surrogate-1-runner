"""
Unit tests for the Router routing logic.
"""

import pytest
from surrogate_1.router import Router, DEFAULT_PROTOCOL_MAP


def test_router_known_protocols():
    router = Router()
    for proto, addr in DEFAULT_PROTOCOL_MAP.items():
        assert router.route(proto) == addr


def test_router_unknown_protocol():
    router = Router()
    assert router.route("unknown-proto") is None