import re
from typing import List, Dict

class CommandResolver:
    def __init__(self, commands: List[str]):
        self.commands = commands
        self.filtered_commands = []

    def filter_commands(self, context: str) -> List[str]:
        """
        Filters commands based on the given context.
        """
        self.filtered_commands = [cmd for cmd in self.commands if context.lower() in cmd.lower()]
        return self.filtered_commands[:5]

    def fuzzy_search(self, query: str) -> List[str]:
        """
        Performs fuzzy search on the filtered commands.
        """
        results = []
        for cmd in self.filtered_commands:
            if re.search(query, cmd, re.IGNORECASE):
                results.append(cmd)
        return results[:5]

    def execute_command(self, command: str) -> None:
        """
        Executes the selected command.
        """
        # Placeholder for command execution logic
        print(f"Executing command: {command}")

# Example usage
if __name__ == "__main__":
    commands = [
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
    resolver = CommandResolver(commands)
    context = "command"
    filtered_commands = resolver.filter_commands(context)
    print("Filtered Commands:", filtered_commands)
    query = "com"
    fuzzy_results = resolver.fuzzy_search(query)
    print("Fuzzy Search Results:", fuzzy_results)
    resolver.execute_command(fuzzy_results[0] if fuzzy_results else "No command found")