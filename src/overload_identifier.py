import re
from typing import List, Optional

class OverloadIdentifier:
    def __init__(self):
        self.type_aliases = {
            'String': 'str',
            'Int': 'int',
            'Float': 'float',
            'Boolean': 'bool',
            'Void': 'None',
        }

    def normalize_type(self, type_str: str) -> str:
        # Handle type aliases
        if type_str in self.type_aliases:
            return self.type_aliases[type_str]

        # Handle generic types
        if '<' in type_str and '>' in type_str:
            base_type, generic_part = type_str.split('<', 1)
            generic_part = generic_part.rsplit('>', 1)[0]
            normalized_base = self.normalize_type(base_type)
            normalized_generic = self.normalize_type(generic_part)
            return f"{normalized_base}<{normalized_generic}>"

        # Handle arrays
        if type_str.endswith('[]'):
            element_type = type_str[:-2]
            normalized_element = self.normalize_type(element_type)
            return f"{normalized_element}[]"

        # Handle inline classes (simplified)
        if '.' in type_str:
            return type_str.split('.')[-1]

        return type_str

    def generate_overload_id(self, function_name: str, parameter_types: List[str]) -> str:
        normalized_types = [self.normalize_type(pt) for pt in parameter_types]
        type_part = '-'.join(normalized_types)
        return f"{function_name}-{type_part}"

    def parse_function_signature(self, signature: str) -> Optional[tuple]:
        # Simplified regex to match function signatures
        pattern = r'^\s*(\w+)\s*\(([^)]*)\)\s*$'
        match = re.match(pattern, signature.strip())
        if not match:
            return None

        function_name = match.group(1)
        parameters = match.group(2).split(',')
        parameter_types = [p.strip() for p in parameters if p.strip()]

        return function_name, parameter_types