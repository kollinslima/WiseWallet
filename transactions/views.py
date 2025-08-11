from django.db.models import Sum
from .forms import TransactionsFileUploadForm
from .models import TradeOperation
from .services import process_transactions_file
from django.core.exceptions import ValidationError
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView

class TransactionsFileUploadFormView(FormView):
    form_class = TransactionsFileUploadForm
    template_name = "transactions/transactions.html"
    success_url = "upload/success"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Summary of trades. 'C' means 'Compra' (Buy)
        summary = TradeOperation.objects.filter(operation='C').values('ticker').annotate(
            total_quantity=Sum('quantity'),
            total_value=Sum('value'),
        ).order_by('ticker')

        # Calculate average price and get institutions for each ticker
        for item in summary:
            item['average_price'] = item['total_value'] / item['total_quantity'] if item['total_quantity'] > 0 else 0
            institutions = TradeOperation.objects.filter(ticker=item['ticker']).values_list('institution', flat=True).distinct()
            item['institutions'] = ", ".join(list(institutions))

        context['summary'] = summary
        return context

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]
        try:
            for f in files:
                process_transactions_file(f)
        except ValidationError as e:
            form.add_error('file_field', e.message)
            return self.form_invalid(form)
        return super().form_valid(form)

class TransactionsFileUploadSuccessView(TemplateView):
    template_name = "transactions/transactions_upload_success.html"


class TransactionDetailView(ListView):
    model = TradeOperation
    template_name = 'transactions/transaction_detail.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        ticker = self.kwargs.get('ticker')
        queryset = TradeOperation.objects.filter(ticker=ticker)

        # Filtering
        filter_operation = self.request.GET.get('filter_operation', '')
        if filter_operation:
            queryset = queryset.filter(operation=filter_operation)

        # Sorting
        sort = self.request.GET.get('sort', '-trade_date')
        valid_sort_fields = ['trade_date', '-trade_date', 'operation', '-operation', 'price', '-price', 'quantity', '-quantity', 'value', '-value']
        if sort in valid_sort_fields:
            queryset = queryset.order_by(sort)
        else:
            queryset = queryset.order_by('-trade_date')


        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort', '-trade_date')
        context['current_filter_operation'] = self.request.GET.get('filter_operation', '')
        context['ticker'] = self.kwargs.get('ticker')
        return context
