"""
Report format utilities for surrogate-1.

Provides concrete implementations for CSV and PDF report generation,
exposed via the `get_report_generator` factory.

Each generator implements a `generate(data: List[Dict[str, Any]]) -> bytes`
method returning the report content as bytes ready for writing to disk or
streaming to a client.

The `data` argument is expected to be a list of dictionaries where each
dictionary represents a row with consistent keys across all rows.
"""

from __future__ import annotations

import csv
import io
from abc import ABC, abstractmethod
from typing import Any, Dict, List

# Optional import for PDF generation. If reportlab is unavailable, raise a clear error.
try:
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
    from reportlab.lib import colors
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "PDF report generation requires the 'reportlab' package. "
        "Install it via `pip install reportlab`."
    ) from exc


class ReportFormat(ABC):
    """Abstract base class for all report formats."""

    @abstractmethod
    def generate(self, data: List[Dict[str, Any]]) -> bytes:
        """
        Generate a report from ``data`` and return it as a ``bytes`` object.

        Args:
            data: A list of dictionaries representing rows. All dictionaries
                  should share the same set of keys.

        Returns:
            The binary representation of the generated report.
        """
        raise NotImplementedError


class CSVReport(ReportFormat):
    """CSV report generator."""

    def generate(self, data: List[Dict[str, Any]]) -> bytes:
        if not data:
            # Return an empty CSV with no header.
            return b""

        output = io.StringIO()
        fieldnames = list(data[0].keys())
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in data:
            writer.writerow(row)

        return output.getvalue().encode("utf-8")


class PDFReport(ReportFormat):
    """PDF report generator using ReportLab."""

    def generate(self, data: List[Dict[str, Any]]) -> bytes:
        if not data:
            # Produce a minimal PDF with a placeholder paragraph.
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=LETTER)
            styles = getSampleStyleSheet()
            elements = [Paragraph("No data available.", styles["Normal"])]
            doc.build(elements)
            return buffer.getvalue()

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=LETTER)
        styles = getSampleStyleSheet()

        # Build table data: header + rows
        header = list(data[0].keys())
        table_data = [header] + [[row.get(col, "") for col in header] for row in data]

        # Create Table with basic styling
        table = Table(table_data, repeatRows=1)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ]
            )
        )

        # Assemble document
        elements = [Paragraph("Cost Allocation Report", styles["Title"]), table]
        doc.build(elements)

        return buffer.getvalue()


def get_report_generator(format_name: str) -> ReportFormat:
    """
    Factory that returns a report generator instance for the requested format.

    Supported format names (case‑insensitive):
        - "csv"
        - "pdf"

    Args:
        format_name: Desired report format.

    Returns:
        An instance of a subclass of :class:`ReportFormat`.

    Raises:
        ValueError: If the format is not supported.
    """
    fmt = format_name.strip().lower()
    if fmt == "csv":
        return CSVReport()
    if fmt == "pdf":
        return PDFReport()
    raise ValueError(f"Unsupported report format: {format_name!r}. Supported: csv, pdf")


__all__ = [
    "ReportFormat",
    "CSVReport",
    "PDFReport",
    "get_report_generator",
]