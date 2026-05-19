import unittest
from core.command_resolver import CommandResolver

class TestCommandResolver(unittest.TestCase):
    def setUp(self):
        self.commands = [
            "command1",
            "command2",
            "command3",
            "command4",
            "command5",
            "command6",
            "command7",
            "command8",
            "command9",
            "command10"
        ]
        self.resolver = CommandResolver(self.commands)

    def test_filter_commands(self):
        context = "command"
        filtered_commands = self.resolver.filter_commands(context)
        self.assertTrue(len(filtered_commands) >= 5)
        for cmd in filtered_commands:
            self.assertIn(context.lower(), cmd.lower())

    def test_fuzzy_search(self):
        query = "com"
        fuzzy_results = self.resolver.fuzzy_search(query)
        self.assertTrue(len(fuzzy_results) >= 5)
        for result in fuzzy_results:
            self.assertTrue(re.search(query, result, re.IGNORECASE))

    def test_execute_command(self):
        command = "command1"
        self.resolver.execute_command(command)
        # Placeholder for assertion based on actual command execution logic

if __name__ == '__main__':
    unittest.main()