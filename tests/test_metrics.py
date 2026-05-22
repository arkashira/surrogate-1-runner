"""
Unit tests for Prometheus metrics integration in playbook generation.
"""

import pytest
from backend.metrics import playbooks_generated_total, active_users_total
from backend.playbook_generator import generate_playbook


@pytest.fixture(autouse=True)
def reset_metrics():
    """
    Reset metric counters before each test to ensure isolation.
    """
    playbooks_generated_total._value.set(0)
    active_users_total._value.set(0)
    yield
    playbooks_generated_total._value.set(0)
    active_users_total._value.set(0)


def test_metrics_increment():
    """
    Verify that generating a playbook increments both counters by one.
    """
    initial_playbooks = playbooks_generated_total._value.get()
    initial_users = active_users_total._value.get()

    generate_playbook(user_id="user123", data={"foo": "bar"})

    assert playbooks_generated_total._value.get() == initial_playbooks + 1
    assert active_users_total._value.get() == initial_users + 1