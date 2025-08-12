from .forms import TransactionsFileUploadForm
from .models import TransactionOperations, AssetIdentification
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

        summary = []

        assets = AssetIdentification.objects.all()
        for asset in assets:
            item = {}
            item['ticker'] = asset.asset_ticker

            asset_buys = (TransactionOperations.objects
                            .filter(asset=asset, operation=TransactionOperations.TransactionOperation.BUY)
                            .aggregate(
                                buy_amount=Sum('amount', default=0),
                                total_buy_value=Sum('total_value', default=0)+Sum('fees', default=0)
                            ))

            asset_sells = (TransactionOperations.objects
                            .filter(asset=asset, operation=TransactionOperations.TransactionOperation.SELL)
                            .aggregate(
                                sell_amount=Sum('amount', default=0)
                            ))

            institutions = (TransactionOperations.objects
                            .filter(asset=asset)
                            .values_list('institution_name', flat=True)
                            .distinct())

            item['amount'] = asset_buys['buy_amount'] - asset_sells['sell_amount']
            item['average_buy_price'] = asset_buys['total_buy_value']/asset_buys['buy_amount']
            item['total_value'] = item['amount']*item['average_buy_price']
            item['institutions'] = ', '.join(institutions)
            summary.append(item)

        context['summary'] = summary
        return context


#  class TransactionDetailView(ListView):
#      model = TransactionOperations
#      template_name = 'transactions/transaction_detail.html'
#      context_object_name = 'object_list'

#      def get_queryset(self):
#          ticker = self.kwargs.get('ticker')
#          queryset = TransactionOperations.objects.filter(ticker=ticker)

#          # Filtering
#          filter_operation = self.request.GET.get('filter_operation', '')
#          if filter_operation:
#              queryset = queryset.filter(operation=filter_operation)

#          # Sorting
#          sort = self.request.GET.get('sort', '-trade_date')
#          valid_sort_fields = ['trade_date', '-trade_date', 'operation', '-operation', 'price', '-price', 'quantity', '-quantity', 'value', '-value']
#          if sort in valid_sort_fields:
#              queryset = queryset.order_by(sort)
#          else:
#              queryset = queryset.order_by('-trade_date')


#          return queryset

#      def get_context_data(self, **kwargs):
#          context = super().get_context_data(**kwargs)
#          context['current_sort'] = self.request.GET.get('sort', '-trade_date')
#          context['current_filter_operation'] = self.request.GET.get('filter_operation', '')
#          context['ticker'] = self.kwargs.get('ticker')
#          return context
