
from django.views.generic import ListView
from ..models import Invoice

class InvoiceListView(ListView):
    model = Invoice
    template_name = 'invoice_list.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        queryset = Invoice.objects.all()
        vendor = self.request.GET.get('vendor')
        date = self.request.GET.get('date')
        amount = self.request.GET.get('amount')

        if vendor:
            queryset = queryset.filter(vendor__icontains=vendor)
        if date:
            queryset = queryset.filter(date__icontains=date)
        if amount:
            queryset = queryset.filter(amount__icontains=amount)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vendor_filter'] = self.request.GET.get('vendor', '')
        context['date_filter'] = self.request.GET.get('date', '')
        context['amount_filter'] = self.request.GET.get('amount', '')
        return context