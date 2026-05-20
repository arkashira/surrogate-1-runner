import json
import sys
from typing import Dict, Any

def format_health_validation_result(is_critical: bool, details: Dict[str, Any]) -> None:
    """
    Formats and outputs health validation results in structured JSON format.
    
    Args:
        is_critical: Boolean indicating if the failure is critical (triggers pipeline failure)
        details: Dictionary containing error details (error message, container_id, timestamp, etc.)
    
    Outputs:
        JSON object with status and details to stdout
    """
    result = {
        "status": "failure" if is_critical else "success",
        "details": details
    }
    
    # Output structured JSON to stdout
    print(json.dumps(result, indent=2))
    
    # Exit with code 1 for critical failures to trigger pipeline failure
    if is_critical:
        sys.exit(1)

if __name__ == "__main__":
    # Example usage - replace with actual validation logic
    is_critical_failure = True  # Determined by your validation logic
    failure_details = {
        "error": "Container health check failed",
        "container_id": "abc123",
        "timestamp": "2023-10-01T12:00:00Z",
        "validation_type": "health_check"
    }
    
    format_health_validation_result(is_critical_failure, failure_details)