import hashlib
from datetime import datetime
from typing import List, Dict, Optional

class DiscrepancyDetector:
    def __init__(self):
        self.duplicate_invoices = set()
        self.unusual_amounts = []
        self.missing_information = []

    def detect_duplicates(self, invoice: Dict) -> bool:
        invoice_hash = hashlib.md5(str(invoice).encode()).hexdigest()
        if invoice_hash in self.duplicate_invoices:
            return True
        self.duplicate_invoices.add(invoice_hash)
        return False

    def detect_unusual_amounts(self, invoice: Dict, threshold: float) -> bool:
        if invoice.get('amount', 0) > threshold:
            self.unusual_amounts.append(invoice)
            return True
        return False

    def detect_missing_information(self, invoice: Dict, required_fields: List[str]) -> bool:
        missing_fields = [field for field in required_fields if field not in invoice]
        if missing_fields:
            self.missing_information.append({
                'invoice': invoice,
                'missing_fields': missing_fields
            })
            return True
        return False

    def detect_discrepancies(self, invoice: Dict, threshold: float, required_fields: List[str]) -> Dict:
        discrepancies = {
            'duplicate': self.detect_duplicates(invoice),
            'unusual_amount': self.detect_unusual_amounts(invoice, threshold),
            'missing_information': self.detect_missing_information(invoice, required_fields)
        }
        return discrepancies