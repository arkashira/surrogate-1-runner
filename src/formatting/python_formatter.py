import autopep8
from typing import Optional, Dict

class PythonFormatter:
    """
    A Python code formatter that uses autopep8 to format code according to configurable style rules.
    """

    DEFAULT_CONFIG = {
        'max_line_length': 88,
        'indent_size': 4,
        'ignore': ['E203', 'E266', 'E704'],
        'aggressive': 1
    }

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the formatter with optional configuration.

        Args:
            config: Dictionary of configuration options. If None, uses default configuration.
        """
        self.config = config or self.DEFAULT_CONFIG.copy()

    def format_code(self, code: str) -> str:
        """
        Format the given Python code according to the configured style.

        Args:
            code: The Python code to format.

        Returns:
            The formatted Python code.
        """
        if not isinstance(code, str):
            raise ValueError("Input code must be a string")

        return autopep8.fix_code(
            code,
            options=self.config
        )

    def get_config(self) -> Dict:
        """
        Get the current configuration for the formatter.

        Returns:
            The current configuration dictionary.
        """
        return self.config.copy()

    def set_config(self, config: Dict) -> None:
        """
        Set the configuration for the formatter.

        Args:
            config: The configuration to use. Will merge with existing config.
        """
        if not isinstance(config, dict):
            raise ValueError("Config must be a dictionary")

        self.config.update(config)

    def reset_config(self) -> None:
        """
        Reset the configuration to default values.
        """
        self.config = self.DEFAULT_CONFIG.copy()