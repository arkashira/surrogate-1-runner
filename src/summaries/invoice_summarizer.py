from typing import Dict, Optional

def generate_invoice_summary(invoice: Dict) -> str:
    """
    Generate a concise summary of an invoice.

    Args:
        invoice: A dictionary containing invoice details.
                 Expected keys: 'vendor_name', 'invoice_date', 'total_amount', 'due_date'.

    Returns:
        A formatted string summarizing the key information.
    """
    vendor_name = invoice.get('vendor_name', 'Unknown Vendor')
    invoice_date = invoice.get('invoice_date', 'Unknown Date')
    total_amount = invoice.get('total_amount', 0.0)
    due_date = invoice.get('due_date', 'Unknown Due Date')

    # Format the summary with clear, concise information
    summary = (
        f"Invoice from {vendor_name}, dated {invoice_date}, "
        f"for a total amount of ${total_amount:.2f}, due on {due_date}."
    )
    return summary