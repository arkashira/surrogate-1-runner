import pytest
from services.roi_service import calculate_roi

def test_high_pricing_scenario():
    # High pricing scenario
    current_fps = 1000
    candidate_fps = 1500
    current_price = 1000.0
    candidate_price = 1200.0
    expected_roi = (1500 / 1200) / (1000 / 1000) - 1
    assert calculate_roi(current_fps, candidate_fps, current_price, candidate_price) == expected_roi

def test_medium_pricing_scenario():
    # Medium pricing scenario
    current_fps = 500
    candidate_fps = 750
    current_price = 500.0
    candidate_price = 600.0
    expected_roi = (750 / 600) / (500 / 500) - 1
    assert calculate_roi(current_fps, candidate_fps, current_price, candidate_price) == expected_roi

def test_low_pricing_scenario():
    # Low pricing scenario
    current_fps = 200
    candidate_fps = 300
    current_price = 200.0
    candidate_price = 240.0
    expected_roi = (300 / 240) / (200 / 200) - 1
    assert calculate_roi(current_fps, candidate_fps, current_price, candidate_price) == expected_roi

def test_edge_case_equal_fps():
    # Edge case where current FPS equals candidate FPS
    current_fps = 400
    candidate_fps = 400
    current_price = 400.0
    candidate_price = 480.0
    assert calculate_roi(current_fps, candidate_fps, current_price, candidate_price) == 0