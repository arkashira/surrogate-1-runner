import os
import time
from datetime import datetime

def generate_invoice_summary(invoice):
    # Placeholder for actual summary generation logic
    summary = f"Invoice {invoice['id']} - Total: ${invoice['total']:.2f}"
    return summary

def process_invoice(invoice):
    start_time = time.time()
    summary = generate_invoice_summary(invoice)
    processing_time = time.time() - start_time
    print(f"Invoice summary generated in {processing_time:.2f} seconds: {summary}")

# /opt/axentx/surrogate-1/invoice_summary_test.py
import unittest
from invoice_summary import generate_invoice_summary, process_invoice

class TestInvoiceSummary(unittest.TestCase):
    def test_generate_invoice_summary(self):
        invoice = {"id": 1, "total": 123.45}
        summary = generate_invoice_summary(invoice)
        self.assertEqual(summary, "Invoice 1 - Total: $123.45")

    def test_process_invoice(self):
        invoice = {"id": 1, "total": 123.45}
        process_invoice(invoice)

if __name__ == '__main__':
    unittest.main()

## Summary
- Implemented `generate_invoice_summary` function to create a basic invoice summary
- Implemented `process_invoice` function to generate the summary and measure processing time
- Created test cases for both functions in `invoice_summary_test.py`