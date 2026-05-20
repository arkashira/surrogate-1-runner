import pytest
from unittest.mock import Mock, patch
from src.onboarding_engine import OnboardingEngine

@pytest.fixture
def mock_db():
    return Mock()

@pytest.fixture
def engine(mock_db):
    return OnboardingEngine(db=mock_db)

def test_load_sequence_and_progress(engine, mock_db):
    # Setup
    user_id = "user123"
    sequence_id = "seq456"
    
    # Mock database calls
    mock_db.get_user_progress.return_value = {"current_step": 1}
    mock_db.get_sequence.return_value = [
        {"step_id": 1, "action": "welcome"},
        {"step_id": 2, "action": "setup_profile"},
        {"step_id": 3, "action": "connect_social"}
    ]
    
    # Test
    result = engine.load_sequence_and_progress(user_id, sequence_id)
    
    # Assert
    assert result == {
        "sequence": [
            {"step_id": 1, "action": "welcome"},
            {"step_id": 2, "action": "setup_profile"},
            {"step_id": 3, "action": "connect_social"}
        ],
        "progress": {"current_step": 1}
    }
    mock_db.get_user_progress.assert_called_once_with(user_id, sequence_id)
    mock_db.get_sequence.assert_called_once_with(sequence_id)

def test_get_next_step(engine, mock_db):
    # Setup
    user_id = "user123"
    sequence_id = "seq456"
    
    # Mock data
    mock_db.get_user_progress.return_value = {"current_step": 1}
    mock_db.get_sequence.return_value = [
        {"step_id": 1, "action": "welcome"},
        {"step_id": 2, "action": "setup_profile"},
        {"step_id": 3, "action": "connect_social"}
    ]
    
    # Test
    result = engine.get_next_step(user_id, sequence_id)
    
    # Assert
    assert result == {"step_id": 2, "action": "setup_profile"}
    mock_db.get_user_progress.assert_called_once_with(user_id, sequence_id)
    mock_db.get_sequence.assert_called_once_with(sequence_id)

def test_get_next_step_completed_sequence(engine, mock_db):
    # Setup
    user_id = "user123"
    sequence_id = "seq456"
    
    # Mock data - user has completed all steps
    mock_db.get_user_progress.return_value = {"current_step": 3}
    mock_db.get_sequence.return_value = [
        {"step_id": 1, "action": "welcome"},
        {"step_id": 2, "action": "setup_profile"},
        {"step_id": 3, "action": "connect_social"}
    ]
    
    # Test
    result = engine.get_next_step(user_id, sequence_id)
    
    # Assert
    assert result is None
    mock_db.get_user_progress.assert_called_once_with(user_id, sequence_id)
    mock_db.get_sequence.assert_called_once_with(sequence_id)

def test_update_user_progress(engine, mock_db):
    # Setup
    user_id = "user123"
    sequence_id = "seq456"
    step_id = 2
    
    # Test
    engine.update_user_progress(user_id, sequence_id, step_id)
    
    # Assert
    mock_db.update_user_progress.assert_called_once_with(user_id, sequence_id, step_id)