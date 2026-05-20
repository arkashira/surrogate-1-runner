
import unittest
from invoice_parser import InvoiceParser

class TestInvoiceParser(unittest.TestCase):
    def test_parse_invoice(self):
        for invoice in INVOICE_SAMPLES:
            parsed_invoice = InvoiceParser().parse(invoice)
            self.assertGreater(len(parsed_invoice), 0)
            self.assertIn('amount_due', parsed_invoice.keys())
            self.assertIn('due_date', parsed_invoice.keys())
            self.assertIn('line_items', parsed_invoice.keys())

    def test_parse_invalid_invoice(self):
        for invoice in INVALID_INVOICE_SAMPLES:
            with self.assertRaises(ValueError):
                InvoiceParser().parse(invoice)

INVOICE_SAMPLES = [
    # Add your test invoice samples here
]

INVALID_INVOICE_SAMPLES = [
    # Add your invalid test invoice samples here
]

if __name__ == '__main__':
    unittest.main()