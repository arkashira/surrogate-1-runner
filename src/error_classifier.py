from typing import Dict, Any

class ErrorClassifier:
    def __init__(self):
        self.error_patterns = {
            "timeout": ["timeout", "timed out"],
            "connection": ["connection", "network"],
            "authentication": ["auth", "credentials"],
            "validation": ["invalid", "validation"],
            "resource": ["resource", "not found"]
        }

    def classify_error(self, error: str) -> str:
        error_lower = error.lower()
        for error_type, patterns in self.error_patterns.items():
            for pattern in patterns:
                if pattern in error_lower:
                    return error_type
        return "unknown"