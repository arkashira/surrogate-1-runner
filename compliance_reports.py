from datetime import datetime
from typing import Dict, List, Optional

class ComplianceReport:
    """
    Represents a compliance report with optional filters (customizations).
    Encapsulates report generation logic for a given set of audit events.
    """
    def __init__(self, report_type: str, audit_trail_data: List[Dict]):
        self.report_type = report_type
        self.audit_trail_data = audit_trail_data
        self.customizations = {}

    def add_customization(self, key: str, value: str) -> None:
        """
        Add a filter criterion (e.g., user='user1') to refine report data.
        """
        self.customizations[key] = value

    def generate_report(self) -> Dict:
        """
        Generate the final report dictionary with metadata and filtered data.
        """
        return {
            "report_type": self.report_type,
            "generated_at": datetime.now().isoformat(),
            "customizations": self.customizations.copy(),
            "data": self._filter_data(),
        }

    def _filter_data(self) -> List[Dict]:
        """
        Filter audit trail entries that match all customization key-value pairs.
        If no customizations, return all data.
        """
        if not self.customizations:
            return self.audit_trail_data

        filtered = []
        for entry in self.audit_trail_data:
            if self._entry_matches(entry):
                filtered.append(entry)
        return filtered

    def _entry_matches(self, entry: Dict) -> bool:
        """
        Check if an audit entry matches all customization filters.
        Only checks keys present in customizations.
        """
        for key, value in self.customizations.items():
            if entry.get(key) != value:
                return False
        return True


class ComplianceReportGenerator:
    """
    High-level interface to generate compliance reports from raw audit data.
    Reusable across report types (GDPR, SOC-2, HIPAA, etc.).
    """
    def __init__(self, audit_trail_data: List[Dict]):
        if not isinstance(audit_trail_data, list):
            raise TypeError("audit_trail_data must be a list of dictionaries")
        self.audit_trail_data = audit_trail_data

    def generate_report(
        self,
        report_type: str,
        customizations: Optional[Dict[str, str]] = None
    ) -> Dict:
        """
        Create a compliance report of the specified type with optional filters.
        """
        report = ComplianceReport(report_type, self.audit_trail_data)
        if customizations:
            for key, value in customizations.items():
                report.add_customization(key, value)
        return report.generate_report()