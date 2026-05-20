import json
from datetime import datetime

class ComplianceReport:
    def __init__(self, security_scan_results, recommendations):
        self.security_scan_results = security_scan_results
        self.recommendations = recommendations
        self.generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_json(self):
        return {
            "security_scan_results": self.security_scan_results,
            "recommendations": self.recommendations,
            "generated_at": self.generated_at
        }

def generate_compliance_report(security_scan_results, recommendations):
    report = ComplianceReport(security_scan_results, recommendations)
    return report.to_json()

def main():
    security_scan_results = [
        {"resource": "resource1", "status": "compliant"},
        {"resource": "resource2", "status": "non-compliant"}
    ]
    recommendations = [
        {"resource": "resource2", "recommendation": "fix vulnerability"}
    ]
    report = generate_compliance_report(security_scan_results, recommendations)
    with open('/opt/axentx/surrogate-1/api/compliance_reports.json', 'w') as f:
        json.dump(report, f, indent=4)

if __name__ == "__main__":
    main()