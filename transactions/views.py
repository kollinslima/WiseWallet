from .forms import TransactionsFileUploadForm
from .models import TradeOperations
from .services import process_transactions_file
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView

class TransactionsFileUploadFormView(FormView):
    form_class = TransactionsFileUploadForm
    template_name = "transactions/transactions_upload.html"
    success_url = reverse_lazy('root')

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]
        try:
            for f in files:
                process_transactions_file(f)
        except ValidationError as e:
            form.add_error('file_field', e.message)
            return self.form_invalid(form)
        return super().form_valid(form)

class TransactionsView(TemplateView):
    template_name = "transactions/transactions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        summary = TradeOperations.objects.all()

        context['summary'] = summary
        return context


class TransactionDetailView(ListView):
    model = TradeOperations
    template_name = 'transactions/transaction_detail.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        ticker = self.kwargs.get('ticker')
        queryset = TradeOperations.objects.filter(ticker=ticker)

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
