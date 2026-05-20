from flask import Blueprint, render_template
from ..models import Invoice

invoice_summary_bp = Blueprint('invoice_summary', __name__)

@invoice_summary_bp.route('/invoices/<int:invoice_id>/summary')
def invoice_summary(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    return render_template('invoice_summary.html',
                         vendor_name=invoice.vendor_name,
                         date=invoice.date,
                         amount=invoice.amount,
                         due_date=invoice.due_date)

@invoice_summary_bp.route('/invoices')
def invoice_list():
    invoices = Invoice.query.all()
    return render_template('invoice_list.html', invoices=invoices)