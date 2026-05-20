import json
from typing import Any, Callable, Dict, Iterable, List, Optional

# Supported operators mapped to callables
_OPERATOR_MAP: Dict[str, Callable[[Any, Any], bool]] = {
    "eq": lambda a, b: a == b,
    "contains": lambda a, b: b in a if isinstance(a, (str, list, tuple, set)) else False,
    "gt": lambda a, b: a > b,
    "lt": lambda a, b: a < b,
}


class AuditRequestFiltering:
    def __init__(self):
        self.filters = []

    def add_filter(self, filter_rule: Dict[str, Any]) -> None:
        """Add a custom filtering rule."""
        self._validate_rule(filter_rule)
        self.filters.append(filter_rule)

    def apply_filters(self, audit_requests: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply filters to the given audit requests."""
        filtered_requests = []
        for request in audit_requests:
            if self._is_request_valid(request):
                filtered_requests.append(request)
        return filtered_requests

    def _is_request_valid(self, request: Dict[str, Any]) -> bool:
        """Check if the request meets all filtering criteria."""
        for filter_rule in self.filters:
            field = filter_rule["field"]
            operator = filter_rule["operator"]
            value = filter_rule["value"]

            # Missing field fails the rule
            if field not in request:
                return False

            operand = request[field]
            op_func = _OPERATOR_MAP[operator]
            if not op_func(operand, value):
                return False
        return True

    @staticmethod
    def _validate_rule(rule: Dict[str, Any]) -> None:
        """Validate rule structure and operator."""
        required_keys = {"field", "operator", "value"}
        if not required_keys.issubset(rule):
            raise ValueError(f"Rule missing required keys: {required_keys - set(rule)}")
        if rule["operator"] not in _OPERATOR_MAP:
            raise ValueError(f"Unsupported operator: {rule['operator']}")

    def to_json(self) -> str:
        """Serialize filters to JSON."""
        return json.dumps(self.filters, indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> "AuditRequestFiltering":
        """Deserialize filters from JSON."""
        filters = json.loads(json_str)
        instance = cls()
        instance.filters = filters
        return instance

# Example usage
if __name__ == "__main__":
    filtering = AuditRequestFiltering()
    filtering.add_filter({"field": "priority", "operator": "eq", "value": "high"})

    # Example audit requests
    audit_requests = [
        {'id': 1, 'priority': 'high'},
        {'id': 2, 'priority': 'low'},
        {'id': 3, 'priority': 'high'},
    ]

    filtered_requests = filtering.apply_filters(audit_requests)
    print(filtered_requests)  # Should print only high priority requests