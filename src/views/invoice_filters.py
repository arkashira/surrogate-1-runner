from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Invoice:
    id: str
    vendor: str
    date: datetime
    amount: float
    description: str
    paid: bool
    notes: str = ""

    @staticmethod
    def from_dict(data: dict) -> 'Invoice':
        return Invoice(
            id=data.get('id'),
            vendor=data.get('vendor'),
            date=datetime.strptime(data.get('date'), '%Y-%m-%d').date(),
            amount=float(data.get('amount', 0)),
            description=data.get('description', ''),
            paid=data.get('paid', False),
            notes=data.get('notes', '')
        )

class InvoiceFilter:
    def __init__(self):
        self.search_query: Optional[str] = None
        self.vendor_filter: Optional[str] = None
        self.date_from: Optional[datetime] = None
        self.date_to: Optional[datetime] = None
        self.min_amount: Optional[float] = None
        self.max_amount: Optional[float] = None
        self.is_paid: Optional[bool] = None

    def apply_filters(self, invoices: List[Invoice]) -> List[Invoice]:
        filtered = []

        for invoice in invoices:
            # Apply search query
            if self.search_query:
                if not self._matches_search(invoice):
                    continue

                # Apply vendor filter
                if self.vendor_filter and invoice.vendor != self.vendor_filter:
                    continue

                # Apply date range filter
                if self.date_from and self.date_to:
                    if invoice.date < self.date_from or invoice.date > self.date_to:
                        continue

                # Apply amount range filter
                if self.min_amount is not None and invoice.amount < self.min_amount:
                    continue
                if self.max_amount is not None and invoice.amount > self.max_amount:
                    continue

                # Apply paid status filter
                if self.is_paid is not None and invoice.paid != self.is_paid:
                    continue

                filtered.append(invoice)

        return filtered

    def _matches_search(self, invoice: Invoice) -> bool:
        if not self.search_query:
            return True

        search = self.search_query.lower()
        # Check vendor name
        if invoice.vendor.lower().find(search) != -1:
            return True
        # Check amount
        if str(invoice.amount).lower().find(search) != -1:
            return True
        # Check date
        if invoice.date.strftime('%Y-%m-%d').lower().find(search) != -1:
            return True
        # Check description
        if invoice.description.lower().find(search) != -1:
            return True

        return False

class InvoiceListView:
    def __init__(self):
        self._invoices = []
        self._filters = InvoiceFilter()

    def set_invoices(self, invoices: List[Dict[str, Any]]):
        self._invoices = [Invoice.from_dict(inv) for inv in invoices]

    def set_filters(self, search_query: Optional[str] = None,
                    vendor_filter: Optional[str] = None,
                    date_from: Optional[datetime] = None,
                    date_to: Optional[datetime] = None,
                    min_amount: Optional[float] = None,
                    max_amount: Optional[float] = None,
                    is_paid: Optional[bool] = None):
        self._filters.search_query = search_query
        self._filters.vendor_filter = vendor_filter
        self._filters.date_from = date_from
        self._filters.date_to = date_to
        self._filters.min_amount = min_amount
        self._filters.max_amount = max_amount
        self._filters.is_paid = is_paid

    def clear_filters(self):
        self._filters = InvoiceFilter()

    def get_filtered_invoices(self) -> List[Invoice]:
        return self._filters.apply_filters(self._invoices)