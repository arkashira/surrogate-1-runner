import json
from typing import Dict, List, Tuple
import markdown

class ReportFormatter:
    def __init__(self, coverage_data: Dict):
        self.coverage_data = coverage_data

    def generate_json_report(self) -> str:
        """Generate JSON report from coverage data."""
        return json.dumps(self.coverage_data, indent=2)

    def generate_markdown_report(self) -> str:
        """Generate Markdown report from coverage data."""
        report = "# Coverage Report\n\n"
        report += f"## Overall Coverage: {self.coverage_data['overall_coverage']}%\n\n"
        report += "## Files with Uncovered Lines\n\n"
        report += "| File | Uncovered Lines | Recommended Tests |\n"
        report += "|------|-----------------|--------------------|\n"

        for file_info in self.coverage_data['files']:
            report += f"| {file_info['file']} | {file_info['uncovered_lines']} | {file_info['recommended_tests']} |\n"

        return markdown.markdown(report)

    def generate_reports(self) -> Tuple[str, str]:
        """Generate both JSON and Markdown reports."""
        json_report = self.generate_json_report()
        markdown_report = self.generate_markdown_report()
        return json_report, markdown_report