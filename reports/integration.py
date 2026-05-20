import json
import csv
from fpdf import FPDF
from datetime import datetime
from surrogate_1.alert_aggregation import get_alerts
from surrogate_1.root_cause_analysis import analyze_root_cause

class IncidentReportGenerator:
    def __init__(self, user_preferences=None):
        self.user_preferences = user_preferences or {}

    def generate_report(self, alert_id):
        alerts = get_alerts(alert_id)
        root_cause = analyze_root_cause(alerts)

        report_data = {
            "alert_id": alert_id,
            "timestamp": datetime.now().isoformat(),
            "alerts": alerts,
            "root_cause": root_cause,
            "user_preferences": self.user_preferences
        }

        return report_data

    def export_to_pdf(self, report_data, output_path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for key, value in report_data.items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

        pdf.output(output_path)

    def export_to_csv(self, report_data, output_path):
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for key, value in report_data.items():
                writer.writerow([key, json.dumps(value)])

# Summary:
# - Integrated incident reports with alert aggregation and root-cause analysis
# - Added methods to export reports in PDF and CSV formats
# - Implemented configurable report generation based on user preferences