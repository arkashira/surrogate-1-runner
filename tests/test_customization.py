import pytest
from src.customization import CustomizationManager

def test_add_and_get_customization():
    manager = CustomizationManager()
    org_id = "test_org"
    custom_settings = {"setting1": "value1"}
    manager.add_customization(org_id, custom_settings)
    assert manager.get_customization(org_id) == custom_settings

def test_update_customization():
    manager = CustomizationManager()
    org_id = "test_org"
    initial_settings = {"setting1": "value1"}
    manager.add_customization(org_id, initial_settings)
    updated_settings = {"setting1": "value2", "setting2": "value2"}
    manager.update_customization(org_id, updated_settings)
    assert manager.get_customization(org_id) == {"setting1": "value2", "setting2": "value2"}

def test_get_nonexistent_customization():
    manager = CustomizationManager()
    assert manager.get_customization("nonexistent_org") is None