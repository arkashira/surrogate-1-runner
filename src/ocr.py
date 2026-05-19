import re
from datetime import datetime
from typing import Dict, Optional, Tuple

import pytesseract
from PIL import Image


class InvoiceOCR:
    """
    A class to perform OCR on invoice images and extract structured data.
    """

    CATEGORIES = {
        "utilities": ["electricity", "water", "gas", "utility", "telecom", "internet", "phone"],
        "services": ["consulting", "software", "maintenance", "support", "subscription", "hosting"],
        "supplies": ["office supplies", "paper", "toner", "cleaning", "materials", "equipment"]
    }

    def __init__(self, language: str = "eng"):
        self.language = language

    def extract_text(self, image_path: str) -> str:
        """
        Perform OCR on the given image and return extracted text.
        """
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang=self.language)
            return text.strip()
        except Exception as e:
            raise RuntimeError(f"OCR extraction failed: {str(e)}")

    def parse_vendor(self, text: str) -> Optional[str]:
        """
        Heuristic-based extraction of vendor name (assumes vendor name is near top of document).
        """
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        # Take first non-empty line as potential vendor (common in invoices)
        return lines[0] if lines else None

    def parse_date(self, text: str) -> Optional[str]:
        """
        Extract invoice date using regex patterns.
        """
        date_patterns = [
            r'\b(\d{4}-\d{2}-\d{2})\b',  # YYYY-MM-DD
            r'\b(\d{2}/\d{2}/\d{4})\b',  # MM/DD/YYYY
            r'\b(\d{2}-\d{2}-\d{4})\b',  # MM-DD-YYYY
            r'\b(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})\b'
        ]
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                date_str = match.group(1)
                # Normalize to ISO format
                try:
                    if '-' in date_str and len(date_str) == 10 and date_str[4] == '-':
                        return date_str  # Already ISO
                    elif '/' in date_str:
                        return datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d")
                    elif '-' in date_str:
                        return datetime.strptime(date_str, "%m-%d-%Y").strftime("%Y-%m-%d")
                    else:
                        return datetime.strptime(date_str, "%d %b %Y").strftime("%Y-%m-%d")
                except ValueError:
                    continue
        return None

    def parse_amount(self, text: str) -> Optional[float]:
        """
        Extract total amount (assumes format like $123.45 or 123.45 USD).
        """
        amount_patterns = [
            r'\$\s*([0-9,]+(?:\.[0-9]{2})?)',  # $123.45 or $1,234.56
            r'([0-9,]+(?:\.[0-9]{2})?)\s*(?:USD|CAD|EUR|GBP)',  # 123.45 USD
            r'total.*?([0-9,]+(?:\.[0-9]{2})?)',  # total: 123.45
        ]
        for pattern in amount_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(',', '')
                try:
                    return float(amount_str)
                except ValueError:
                    continue
        return None

    def parse_due_date(self, text: str) -> Optional[str]:
        """
        Extract due date using keywords like 'Due Date' or 'Payment Due'.
        """
        due_date_keywords = ['due date', 'payment due', 'pay by', 'deadline']
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in due_date_keywords):
                return self.parse_date(line)
        return None

    def categorize(self, text: str) -> str:
        """
        Categorize invoice based on keywords in the text.
        """
        text_lower = text.lower()
        for category, keywords in self.CATEGORIES.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
        return "other"

    def process_invoice(self, image_path: str) -> Dict:
        """
        Full pipeline: OCR -> parse fields -> categorize -> return structured data.
        """
        raw_text = self.extract_text(image_path)

        return {
            "vendor_name": self.parse_vendor(raw_text),
            "invoice_date": self.parse_date(raw_text),
            "amount": self.parse_amount(raw_text),
            "due_date": self.parse_due_date(raw_text),
            "category": self.categorize(raw_text),
            "raw_text": raw_text  # For debugging/audit
        }