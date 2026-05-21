import json
import csv
from typing import Dict, List, Union
from dataclasses import dataclass
from pathlib import Path

@dataclass
class CoverageData:
    file_path: str
    covered_lines: List[int]
    uncovered_lines: List[int]
    coverage_percentage: float

class ReportExporter:
    def __init__(self, coverage_data: List[CoverageData]):
        self.coverage_data = coverage_data

    def export_to_html(self, output_path: str) -> None:
        html_content = self._generate_html_report()
        with open(output_path, 'w') as f:
            f.write(html_content)

    def export_to_json(self, output_path: str) -> None:
        json_data = self._generate_json_report()
        with open(output_path, 'w') as f:
            json.dump(json_data, f, indent=4)

    def export_to_csv(self, output_path: str) -> None:
        csv_data = self._generate_csv_report()
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)

    def _generate_html_report(self) -> str:
        html = "<html><head><title>Coverage Report</title></head><body>"
        html += "<h1>Coverage Report</h1>"
        html += "<table border='1'><tr><th>File</th><th>Covered Lines</th><th>Uncovered Lines</th><th>Coverage %</th></tr>"
        for data in self.coverage_data:
            html += f"<tr><td>{data.file_path}</td><td>{', '.join(map(str, data.covered_lines))}</td><td>{', '.join(map(str, data.uncovered_lines))}</td><td>{data.coverage_percentage:.2f}%</td></tr>"
        html += "</table></body></html>"
        return html

    def _generate_json_report(self) -> List[Dict[str, Union[str, List[int], float]]]:
        return [{
            "file_path": data.file_path,
            "covered_lines": data.covered_lines,
            "uncovered_lines": data.uncovered_lines,
            "coverage_percentage": data.coverage_percentage
        } for data in self.coverage_data]

    def _generate_csv_report(self) -> List[List[Union[str, int, float]]]:
        csv_data = [["File", "Covered Lines", "Uncovered Lines", "Coverage %"]]
        for data in self.coverage_data:
            csv_data.append([
                data.file_path,
                ', '.join(map(str, data.covered_lines)),
                ', '.join(map(str, data.uncovered_lines)),
                f"{data.coverage_percentage:.2f}"
            ])
        return csv_data