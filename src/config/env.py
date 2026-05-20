import os
from typing import Optional

class EnvConfig:
    def __init__(self):
        self.surrogate_struct_output_enabled = self._parse_surrogate_struct_output_enabled()

    def _parse_surrogate_struct_output_enabled(self) -> bool:
        value = os.getenv('SURROGATE_STRUCT_OUTPUT_ENABLED', 'false')
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        else:
            print(f"Warning: Invalid value for SURROGATE_STRUCT_OUTPUT_ENABLED: '{value}'. Defaulting to 'false'.")
            return False

    def is_structured_output_enabled(self) -> bool:
        return self.surrogate_struct_output_enabled

# Example usage:
# config = EnvConfig()
# if config.is_structured_output_enabled():
#     # Activate the entire rewrite pipeline
#     pass