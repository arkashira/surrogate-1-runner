import xml.etree.ElementTree as ET
import json
import os
import sys

COBERTURA_NS = "http://cobertura.sourceforge.net/xml/coverage-04.dtd"


def parse_coverage_xml(xml_path):
    """Parse Cobertura coverage.xml and return structured data."""
    if not os.path.exists(xml_path):
        raise FileNotFoundError(f"Coverage file not found: {xml_path}")

    try:
        tree = ET.parse(xml_path)
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML format in {xml_path}: {str(e)}")

    root = tree.getroot()
    files_data = {}

    # Handle namespace-aware element finding
    def find_ns(tag):
        return f"{{{COBERTURA_NS}}}{tag}"

    for file_elem in root.findall(find_ns("file")):
        file_path = file_elem.get("name")
        if not file_path:
            continue

        # Calculate uncovered lines
        total_lines = int(file_elem.get("lines", 0))
        covered_lines = sum(1 for line in file_elem.findall(find_ns("line")) 
                          if int(line.get("hits", 0)) > 0)
        uncovered_lines = total_lines - covered_lines

        # Extract line numbers of uncovered lines
        line_numbers = [
            int(line.get("number"))
            for line in file_elem.findall(find_ns("line"))
            if int(line.get("hits", 0)) == 0
        ]

        module_name = os.path.splitext(os.path.basename(file_path))[0]
        files_data[module_name] = {
            "total_lines": total_lines,
            "covered_lines": covered_lines,
            "uncovered_lines": uncovered_lines,
            "uncovered_line_numbers": line_numbers
        }

    return files_data


def generate_coverage_gaps_report(input_path, output_path):
    """Generate coverage gaps JSON report."""
    try:
        data = parse_coverage_xml(input_path)
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error generating coverage report: {str(e)}", file=sys.stderr)
        return False


if __name__ == "__main__":
    input_file = "coverage.xml"
    output_file = "coverage_gaps.json"
    
    success = generate_coverage_gaps_report(input_file, output_file)
    if not success:
        sys.exit(1)