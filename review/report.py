"""
Review report generation module.

This module provides a `ReviewReport` class that aggregates all issues
found during a review run, validates and sanitizes user inputs, and renders them into a single HTML report.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any
from jinja2 import Environment, FileSystemLoader
from markdown import markdown

class ReviewReport:
    """
    Collects review issues, validates user inputs, and renders them into an HTML report.

    Attributes
    ----------
    output_dir : Path
        Directory where the report files will be written.
    issues : List[Dict[str, Any]]
        List of issue dictionaries collected during the review.
    """

    def __init__(self, output_dir: str | Path = "review_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.issues: List[Dict[str, Any]] = []

    def validate_issue(self, issue: Dict[str, Any]) -> bool:
        """
        Validate the issue dictionary to ensure it contains the required keys and has valid data types.

        Parameters
        ----------
        issue : dict
            A dictionary containing issue details.

        Returns
        -------
        bool
            True if the issue is valid, False otherwise.
        """
        required_keys = {"id", "description", "file"}
        if not all(key in issue for key in required_keys):
            return False

        if not isinstance(issue["id"], str) or not isinstance(issue["description"], str) or not isinstance(issue["file"], str):
            return False

        if "line" in issue and not isinstance(issue["line"], int):
            return False

        if "link" in issue and not isinstance(issue["link"], str):
            return False

        return True

    def add_issue(self, issue: Dict[str, Any]) -> None:
        """
        Add a single issue to the report after validating its data.

        Parameters
        ----------
        issue : dict
            A dictionary containing issue details.
        """
        if self.validate_issue(issue):
            self.issues.append(issue)
        else:
            print(f"Invalid issue data: {issue}")

    def generate_html(self, template_path: str | Path = "review/templates/report.html") -> str:
        """
        Render the collected issues into an HTML string using Jinja2 and Markdown for better formatting.

        Parameters
        ----------
        template_path : str | Path
            Path to the Jinja2 template file.

        Returns
        -------
        str
            Rendered HTML content.
        """
        env = Environment(loader=FileSystemLoader(Path(template_path).parent), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(Path(template_path).name)
        issues_with_formatted_description = [(issue["id"], markdown(issue["description"])) for issue in self.issues]
        return template.render(issues=issues_with_formatted_description)

    # ... (write_html, write_json, and clear methods remain the same)