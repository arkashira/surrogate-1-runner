import re
import json
from typing import List, Dict, Tuple

class TransactionLogParser:
    def __init__(self, log_file_path: str):
        self.log_file_path = log_file_path

    def extract_code_snippets(self) -> List[Dict[str, str]]:
        """
        Extracts SQL code snippets from transaction logs.

        Returns:
            List of dictionaries containing the severity, SQL pattern, and code snippet.
        """
        code_snippets = []
        severity_pattern = re.compile(r'Severity: (\w+)')
        sql_pattern_pattern = re.compile(r'SQL Pattern: (.+)')
        code_snippet_pattern = re.compile(r'Code Snippet:\n((?:.+\n)+)')

        with open(self.log_file_path, 'r') as file:
            log_content = file.read()

        severity_matches = severity_pattern.finditer(log_content)
        sql_pattern_matches = sql_pattern_pattern.finditer(log_content)
        code_snippet_matches = code_snippet_pattern.finditer(log_content)

        for severity_match, sql_pattern_match, code_snippet_match in zip(severity_matches, sql_pattern_matches, code_snippet_matches):
            severity = severity_match.group(1)
            sql_pattern = sql_pattern_match.group(1)
            code_snippet = code_snippet_match.group(1).strip()

            code_snippets.append({
                'severity': severity,
                'sql_pattern': sql_pattern,
                'code_snippet': code_snippet
            })

        return code_snippets

    def categorize_discrepancies(self, code_snippets: List[Dict[str, str]]) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
        """
        Categorizes discrepancies by severity.

        Args:
            code_snippets: List of dictionaries containing the severity, SQL pattern, and code snippet.

        Returns:
            Tuple of lists containing the critical/blocker and warning discrepancies.
        """
        critical_blocker = []
        warning = []

        for snippet in code_snippets:
            if snippet['severity'].lower() in ['critical', 'blocker']:
                critical_blocker.append(snippet)
            elif snippet['severity'].lower() == 'warning':
                warning.append(snippet)

        return critical_blocker, warning

    def export_findings(self, findings: List[Dict[str, str]], export_format: str, output_file_path: str) -> None:
        """
        Exports findings in the specified format.

        Args:
            findings: List of dictionaries containing the severity, SQL pattern, and code snippet.
            export_format: Format to export the findings (JSON or Markdown).
            output_file_path: Path to the output file.
        """
        if export_format.lower() == 'json':
            with open(output_file_path, 'w') as file:
                json.dump(findings, file, indent=4)
        elif export_format.lower() == 'markdown':
            with open(output_file_path, 'w') as file:
                for finding in findings:
                    file.write(f"### Severity: {finding['severity']}\n")
                    file.write(f"### SQL Pattern: {finding['sql_pattern']}\n")
                    file.write("