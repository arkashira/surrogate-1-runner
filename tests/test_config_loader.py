import pytest
import tempfile
import os
from unittest.mock import patch
from src.config_loader import load_config

def test_load_valid_config():
    """Test loading a valid configuration file"""
    config_content = """
relay_endpoint: "https://relay.example.com"
jwt_secret: "test-secret"
chain_rpc_urls:
  ethereum: "https://ethereum.example.com"
  polygon: "https://polygon.example.com"
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_content)
        temp_path = f.name
    
    try:
        result = load_config(temp_path)
        assert result is not None
        assert result['relay_endpoint'] == "https://relay.example.com"
        assert result['jwt_secret'] == "test-secret"
        assert 'ethereum' in result['chain_rpc_urls']
    finally:
        os.unlink(temp_path)

def test_missing_required_fields():
    """Test that missing required fields are detected"""
    config_content = """
relay_endpoint: "https://relay.example.com"
# jwt_secret is missing
chain_rpc_urls:
  ethereum: "https://ethereum.example.com"
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_content)
        temp_path = f.name
    
    try:
        result = load_config(temp_path)
        assert result is None
    finally:
        os.unlink(temp_path)

def test_invalid_yaml_format():
    """Test handling of invalid YAML format"""
    config_content = """
relay_endpoint: "https://relay.example.com"
jwt_secret: "test-secret"
chain_rpc_urls:
  ethereum: "https://ethereum.example.com"
  polygon: "https://polygon.example.com"
invalid: yaml: content
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_content)
        temp_path = f.name
    
    try:
        result = load_config(temp_path)
        assert result is None
    finally:
        os.unlink(temp_path)

def test_file_not_found():
    """Test handling when config file doesn't exist"""
    result = load_config("nonexistent.yaml")
    assert result is None