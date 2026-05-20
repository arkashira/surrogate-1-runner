import json
from datetime import datetime
from typing import Dict, List, Optional

class RootCauseAnalysis:
    def __init__(self):
        self.incident_reports = {}

    def analyze_incident(self, incident_id: str, incident_data: Dict) -> Dict:
        """
        Analyze the incident and generate root cause insights.

        Args:
            incident_id (str): The unique identifier for the incident.
            incident_data (Dict): The data related to the incident.

        Returns:
            Dict: The root cause insights and recommendations.
        """
        root_cause = self._determine_root_cause(incident_data)
        recommendations = self._generate_recommendations(root_cause)

        report = {
            "incident_id": incident_id,
            "timestamp": datetime.now().isoformat(),
            "root_cause": root_cause,
            "recommendations": recommendations,
            "status": "analyzed"
        }

        self.incident_reports[incident_id] = report
        return report

    def _determine_root_cause(self, incident_data: Dict) -> str:
        """
        Determine the root cause of the incident based on the incident data.

        Args:
            incident_data (Dict): The data related to the incident.

        Returns:
            str: The root cause of the incident.
        """
        # Placeholder logic to determine root cause
        if "error" in incident_data:
            return "System error"
        elif "timeout" in incident_data:
            return "Timeout issue"
        else:
            return "Unknown root cause"

    def _generate_recommendations(self, root_cause: str) -> List[str]:
        """
        Generate recommendations based on the root cause.

        Args:
            root_cause (str): The root cause of the incident.

        Returns:
            List[str]: A list of recommendations.
        """
        recommendations = []
        if root_cause == "System error":
            recommendations.append("Check system logs for detailed error messages.")
            recommendations.append("Restart the affected services.")
        elif root_cause == "Timeout issue":
            recommendations.append("Optimize database queries.")
            recommendations.append("Increase timeout thresholds.")
        else:
            recommendations.append("Investigate further to determine the root cause.")
        return recommendations

    def get_incident_report(self, incident_id: str) -> Optional[Dict]:
        """
        Retrieve the incident report for a given incident ID.

        Args:
            incident_id (str): The unique identifier for the incident.

        Returns:
            Optional[Dict]: The incident report if found, otherwise None.
        """
        return self.incident_reports.get(incident_id)