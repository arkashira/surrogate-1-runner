import unittest
from unittest.mock import patch
from opt.axentx.services.langchain_tools import (
    LANGCHAIN_TOOL_WHITELIST,
    is_langchain_tool,
    detect_langchain_tool_calls
)

class TestLangChainTools(unittest.TestCase):
    def test_whitelist_coverage(self):
        """Test that all whitelisted tools are recognized."""
        for tool in LANGCHAIN_TOOL_WHITELIST:
            self.assertTrue(is_langchain_tool(tool))

    def test_non_whitelisted_tool(self):
        """Test that non-whitelisted tools are rejected."""
        self.assertFalse(is_langchain_tool("non_existent_tool"))

    def test_detect_tool_calls(self):
        """Test detection of tool calls in a payload."""
        test_cases = [
            ([{'name': 'search'}, {'name': 'calculate'}], ['search', 'calculate']),
            ([{'name': 'search'}, {'name': 'unknown'}], ['search']),
            ([{'name': 'unknown'}], []),
            ([], [])
        ]

        for input_calls, expected in test_cases:
            with self.subTest(input_calls=input_calls):
                result = detect_langchain_tool_calls(input_calls)
                self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()