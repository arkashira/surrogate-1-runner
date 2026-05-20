import json
from typing import List, Dict

def serialize_to_sarif(scan_findings: List[Dict]) -> str:
    sarif_report = {
        "$schema": "https://json.schemastore.org/sarif-2.1.0",
        "version": 2,
        "runs": [{
            "tool": {
                "driver": {
                    "name": "AxentX Scanner",
                    "version": "1.0.0",
                    "informationUri": "https://axentx.com",
                    "rules": []
                }
            },
            "results": []
        }]
    }

    for finding in scan_findings:
        result = {
            "ruleId": finding.get("rule_id"),
            "message": {
                "text": finding.get("message")
            },
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {
                        "uri": finding.get("file")
                    },
                    "region": {
                        "startLine": finding.get("line"),
                        "startColumn": 1
                    }
                }
            }]
        }
        sarif_report["runs"][0]["results"].append(result)

    return json.dumps(sarif_report, indent=2)

def save_sarif_report(report: str, file_path: str) -> None:
    with open(file_path, 'w') as file:
        file.write(report)