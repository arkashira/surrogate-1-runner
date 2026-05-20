"""Unit tests for the LLMResponse dataclass."""

import unittest
from src.response import LLMResponse


class TestLLMResponse(unittest.TestCase):
    """Test suite for LLMResponse functionality."""

    def test_init_with_valid_fields(self):
        """Verify instance creation with valid arguments."""
        response = LLMResponse(
            text="example text",
            usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
            finish_reason="stop"
        )
        self.assertEqual(response.text, "example text")
        self.assertEqual(response.usage["total_tokens"], 15)
        self.assertEqual(response.finish_reason, "stop")

    def test_to_dict_returns_correct_structure(self):
        """Verify to_dict produces expected dictionary output."""
        response = LLMResponse(
            text="example text",
            usage={"prompt_tokens": 10, "completion_tokens": 5},
            finish_reason="length"
        )
        result = response.to_dict()
        
        expected = {
            "text": "example text",
            "usage": {"prompt_tokens": 10, "completion_tokens": 5},
            "finish_reason": "length"
        }
        self.assertEqual(result, expected)

    def test_to_dict_is_json_serializable(self):
        """Verify to_dict output can be serialized to JSON."""
        import json
        
        response = LLMResponse(
            text="test",
            usage={"total_tokens": 1},
            finish_reason="stop"
        )
        # Should not raise
        json_str = json.dumps(response.to_dict())
        parsed = json.loads(json_str)
        
        self.assertEqual(parsed["text"], "test")

    def test_usage_with_complex_nested_structure(self):
        """Verify asdict handles nested usage data correctly."""
        response = LLMResponse(
            text="test",
            usage={
                "tokens": {"prompt": 5, "completion": 3},
                "cost": {"currency": "USD", "amount": 0.001}
            },
            finish_reason="stop"
        )
        result = response.to_dict()
        
        self.assertEqual(result["usage"]["tokens"]["prompt"], 5)
        self.assertEqual(result["usage"]["cost"]["amount"], 0.001)


if __name__ == "__main__":
    unittest.main()