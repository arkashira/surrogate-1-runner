import pytest
import json

def test_get_roth_guide_returns_valid_structure(client):
    """Test guide endpoint returns ordered steps with required fields and valid references"""
    response = client.get("/api/roth/guide")
    assert response.status_code == 200
    
    data = response.json
    assert isinstance(data, list), "Response should be an array of steps"
    
    for step in data:
        assert "title" in step and isinstance(step["title"], str), "Each step must have a title string"
        assert "description" in step and isinstance(step["description"], str), "Each step must have a description string"
        assert "references" in step and isinstance(step["references"], list), "Each step must have a references array"
        
        for ref in step["references"]:
            assert isinstance(ref, str) and "irs.gov" in ref, "References must be IRS publication URLs"