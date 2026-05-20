import json
from typing import Dict, List, Tuple

class SeverityClassifier:
    def __init__(self, severity_rules: Dict[str, List[str]]):
        self.severity_rules = severity_rules

    def classify_severity(self, discrepancies: List[Dict]) -> List[Dict]:
        classified_discrepancies = []
        for discrepancy in discrepancies:
            severity = self._determine_severity(discrepancy)
            discrepancy['severity'] = severity
            classified_discrepancies.append(discrepancy)
        return classified_discrepancies

    def _determine_severity(self, discrepancy: Dict) -> str:
        for severity, patterns in self.severity_rules.items():
            for pattern in patterns:
                if pattern in discrepancy.get('sql_pattern', ''):
                    return severity
        return 'warning'

    def export_to_json(self, discrepancies: List[Dict], file_path: str) -> None:
        with open(file_path, 'w') as f:
            json.dump(discrepancies, f, indent=4)

    def export_to_markdown(self, discrepancies: List[Dict], file_path: str) -> None:
        with open(file_path, 'w') as f:
            f.write("# High-Risk Transaction Patterns\n\n")
            for discrepancy in discrepancies:
                f.write(f"## Severity: {discrepancy['severity']}\n")
                f.write(f"### SQL Pattern:\n