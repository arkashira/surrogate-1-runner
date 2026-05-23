import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import time
import json
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ErrorScenario:
    error_type: str
    description: str
    recovery_options: List[str]
    frequency: int = 0

class ErrorAnalyzer:
    def __init__(self):
        self.error_scenarios = {
            "malformed_json": ErrorScenario(
                error_type="Malformed JSON",
                description="The input data is not valid JSON.",
                recovery_options=[
                    "Skip the malformed record and continue processing.",
                    "Log the error and retry with a corrected input.",
                ],
            ),
            "missing_required_field": ErrorScenario(
                error_type="Missing Required Field",
                description="A required field is missing in the input data.",
                recovery_options=[
                    "Skip the record and continue processing.",
                    "Log the error and notify the data provider.",
                ],
            ),
            "invalid_data_type": ErrorScenario(
                error_type="Invalid Data Type",
                description="The data type of a field is invalid.",
                recovery_options=[
                    "Convert the data type if possible.",
                    "Skip the record and continue processing.",
                ],
            ),
            "network_timeout": ErrorScenario(
                error_type="Network Timeout",
                description="A network request timed out.",
                recovery_options=[
                    "Retry the request with exponential backoff.",
                    "Log the error and continue processing.",
                ],
            ),
            "rate_limit_exceeded": ErrorScenario(
                error_type="Rate Limit Exceeded",
                description="The API rate limit has been exceeded.",
                recovery_options=[
                    "Wait for the rate limit to reset.",
                    "Distribute requests more evenly over time.",
                ],
            ),
            "authentication_failed": ErrorScenario(
                error_type="Authentication Failed",
                description="Authentication credentials are invalid or missing.",
                recovery_options=[
                    "Verify and update the authentication credentials.",
                    "Log the error and stop processing until credentials are corrected.",
                ],
            ),
            "data_integrity_check_failed": ErrorScenario(
                error_type="Data Integrity Check Failed",
                description="The data failed an integrity check.",
                recovery_options=[
                    "Skip the record and continue processing.",
                    "Log the error and notify the data provider.",
                ],
            ),
            "unsupported_operation": ErrorScenario(
                error_type="Unsupported Operation",
                description="An unsupported operation was attempted.",
                recovery_options=[
                    "Skip the operation and continue processing.",
                    "Log the error and notify the system administrator.",
                ],
            ),
        }
        self.error_stats = defaultdict(int)

    def analyze_error(self, error_message: str) -> Optional[ErrorScenario]:
        for error_type, scenario in self.error_scenarios.items():
            if error_type in error_message.lower():
                self.error_stats[error_type] += 1
                return scenario
        return None

    def get_common_errors(self, threshold: int = 5) -> List[Tuple[str, int]]:
        return [(error_type, count) for error_type, count in self.error_stats.items() if count >= threshold]

    def log_error(self, error_message: str) -> None:
        scenario = self.analyze_error(error_message)
        if scenario:
            logger.error(f"Error detected: {scenario.error_type} - {scenario.description}")
            logger.info(f"Recovery options: {', '.join(scenario.recovery_options)}")
        else:
            logger.error(f"Unknown error detected: {error_message}")

    def process_data_stream(self, data_stream: List[Dict]) -> None:
        start_time = time.time()
        for record in data_stream:
            try:
                # Simulate processing the record
                self.process_record(record)
            except Exception as e:
                self.log_error(str(e))
        end_time = time.time()
        logger.info(f"Processing time: {end_time - start_time} seconds")

    def process_record(self, record: Dict) -> None:
        # Simulate processing a record
        pass

    def generate_error_report(self) -> Dict:
        return {
            "error_stats": dict(self.error_stats),
            "common_errors": self.get_common_errors(),
            "total_errors": sum(self.error_stats.values()),
        }

def main():
    analyzer = ErrorAnalyzer()
    # Simulate a data stream
    data_stream = [
        {"data": "valid_data"},
        {"data": "invalid_data"},
        {"data": "missing_field"},
        {"data": "invalid_type"},
    ]
    analyzer.process_data_stream(data_stream)
    report = analyzer.generate_error_report()
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()