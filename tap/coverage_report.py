import os
import subprocess
import json
from datetime import datetime

def generate_coverage_report():
    # Execute coverage command to get the current coverage data
    result = subprocess.run(['coverage', 'report', '--json'], capture_output=True, text=True)
    coverage_data = json.loads(result.stdout)

    # Prepare the report content
    report_content = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "coverage_summary": {},
        "missing_coverage": []
    }

    for module, data in coverage_data.items():
        report_content["coverage_summary"][module] = {
            "covered_lines": data["covered_lines"],
            "num_statements": data["num_statements"],
            "percent_covered": data["percent_covered"]
        }
        
        if data["percent_covered"] < 100:
            report_content["missing_coverage"].append({
                "module": module,
                "missing_lines": data["missing_lines"]
            })

    # Write the report to a file
    report_filename = f"coverage_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_filename, 'w') as report_file:
        json.dump(report_content, report_file, indent=4)

    print(f"Coverage report generated: {report_filename}")

if __name__ == "__main__":
    generate_coverage_report()