import pytest
from src.proxy.tool_call_mapper import map_response_to_tool_calls


def test_basic_mapping():
    response = {
        "response_format": {"type": "json_object"},
        "content": '{"name":"search","arguments":"{\\"query\\":\\"python\\"}"}',
    }
    expected = {
        "tool_calls": [
            {
                "function": {
                    "name": "search",
                    "arguments": '{"query":"python"}',
                }
            }
        ]
    }
    assert map_response_to_tool_calls(response) == expected


def test_whitespace_and_newlines():
    response = {
        "response_format": {"type": "json_object"},
        "content": """
            {
                "name": "fetch",
                "arguments": "{\\"id\\": 42}"
            }
        """,
    }
    expected = {
        "tool_calls": [
            {
                "function": {
                    "name": "fetch",
                    "arguments": '{"id": 42}',
                }
            }
        ]
    }
    assert map_response_to_tool_calls(response) == expected


def test_missing_response_format():
    response = {"content": '{"name":"search","arguments":"{\\"query\\":\\"python\\"}"}'}
    assert map_response_to_tool_calls(response) is None


def test_invalid_json_content():
    response = {
        "response_format": {"type": "json_object"},
        "content": "not a json",
    }
    with pytest.raises(ValueError):
        map_response_to_tool_calls(response)


def test_missing_required_keys():
    response = {
        "response_format": {"type": "json_object"},
        "content": '{"name":"search"}',
    }
    with pytest.raises(ValueError):
        map_response_to_tool_calls(response)