import pytest
from pathlib import Path

from collaboration.participant_manager import ParticipantManager, ParticipantAlreadyExistsError, ParticipantNotFoundError


@pytest.fixture
def manager(tmp_path: Path):
    # Create a temporary config file with a low max participants limit for testing
    cfg_path = tmp_path / "config.yaml"
    cfg_path.write_text("max_participants: 3\n", encoding="utf-8")
    return ParticipantManager(config_path=cfg_path)


def test_add_and_list_participants(manager: ParticipantManager):
    manager.add_participant("alice")
    manager.add_participant("bob")
    assert manager.list_participants() == ["alice", "bob"]


def test_add_duplicate_raises(manager: ParticipantManager):
    manager.add_participant("charlie")
    with pytest.raises(ParticipantAlreadyExistsError):
        manager.add_participant("charlie")


def test_remove_participant(manager: ParticipantManager):
    manager.add_participant("dave")
    manager.remove_participant("dave")
    assert manager.list_participants() == []


def test_remove_nonexistent_raises(manager: ParticipantManager):
    with pytest.raises(ParticipantNotFoundError):
        manager.remove_participant("eve")


def test_max_participants_limit(manager: ParticipantManager):
    manager.add_participant("u1")
    manager.add_participant("u2")
    manager.add_participant("u3")
    with pytest.raises(Exception) as exc:
        manager.add_participant("u4")
    assert "max participants" in str(exc.value).lower()