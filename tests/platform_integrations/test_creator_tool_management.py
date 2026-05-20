import unittest
from unittest.mock import Mock
from src.platform_integrations.creator_tool_management import CreatorToolManagement

class TestCreatorToolManagement(unittest.TestCase):
    def test_add_tool(self):
        creator_tool_management = CreatorToolManagement()
        creator_tool_management.add_tool("tool1", "Tool 1")
        self.assertEqual(creator_tool_management.tools, {"tool1": "Tool 1"})

    def test_remove_tool(self):
        creator_tool_management = CreatorToolManagement()
        creator_tool_management.add_tool("tool1", "Tool 1")
        creator_tool_management.remove_tool("tool1")
        self.assertEqual(creator_tool_management.tools, {})

# path/to/tests/platform_integrations/test_creator_tool_management.py