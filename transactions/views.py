import logging

from django.db.models import DecimalField

import logging

from django.db.models import DecimalField

from .forms import TransactionsFileUploadForm
from .models import TransactionOperations, AssetIdentification
from .models import TransactionOperations, AssetIdentification
from .services import process_transactions_file
from decimal import InvalidOperation
from decimal import InvalidOperation
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView

logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

class TransactionsFileUploadFormView(FormView):
    form_class = TransactionsFileUploadForm
    template_name = "transactions/transactions_upload.html"
    success_url = reverse_lazy('transactions:index')

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

            asset_buys = (TransactionOperations.objects
                            .filter(asset=asset, operation=TransactionOperations.TransactionOperation.BUY)
                            .aggregate(
                                buy_amount=Sum(
                                    'amount', 
                                    default=0, 
                                    output_field=DecimalField(max_digits=30, decimal_places=18)),
                                total_buy_value=Sum(
                                        'total_value', 
                                        default=0, 
                                        output_field=DecimalField(max_digits=12, decimal_places=2)),
                                total_buy_fees=Sum(
                                        'fees', 
                                        default=0,
                                        output_field=DecimalField(max_digits=12, decimal_places=2))
                            ))

            asset_sells = (TransactionOperations.objects
                            .filter(asset=asset, operation=TransactionOperations.TransactionOperation.SELL)
                            .aggregate(
                                sell_amount=Sum(
                                    'amount',
                                    default=0,
                                    output_field=DecimalField(max_digits=30, decimal_places=18)),
                            ))

            institutions = (TransactionOperations.objects
                            .filter(asset=asset)
                            .values_list('institution_name', flat=True)
                            .distinct())

            item = {}
            item['ticker'] = asset.asset_ticker
            item['amount'] = asset_buys['buy_amount'] - asset_sells['sell_amount']
            item['institutions'] = ', '.join(institutions)

            try:
                item['average_buy_price'] = (asset_buys['total_buy_value'] + asset_buys['total_buy_fees'])/asset_buys['buy_amount']
            except InvalidOperation:
                item['average_buy_price'] = 0

            item['total_value'] = item['amount']*item['average_buy_price']
            summary.append(item)

        context['summary'] = summary
        return context


class TransactionDetailView(ListView):
    model = TransactionOperations
    context_object_name = "transactions"
    template_name = "transactions/transaction_detail.html"

    def get_queryset(self):
        ticker = self.kwargs.get('ticker')
        queryset = TransactionOperations.objects.filter(asset__asset_ticker=ticker)

        # Filtering
        filter_operation = self.request.GET.get('filter_operation', '')
        if filter_operation:
            queryset = queryset.filter(operation=filter_operation)

        # Sorting
        sort = self.request.GET.get('sort', '-settlement_date')
        valid_sort_fields = ['settlement_date', '-settlement_date', 'operation', '-operation', 'amount', '-amount', 'total_value', '-total_value']
        if sort in valid_sort_fields:
            queryset = queryset.order_by(sort)
        else:
            queryset = queryset.order_by('-settlement_date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #  context['current_sort'] = self.request.GET.get('sort', '-settlement_date')
        #  context['current_filter_operation'] = self.request.GET.get('filter_operation', '')
        context['ticker'] = self.kwargs.get('ticker')
        return context
class TransactionsView(TemplateView):
    template_name = "transactions/transactions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        summary = []

        assets = AssetIdentification.objects.all()
        for asset in assets:

            asset_buys = (TransactionOperations.objects
                            .filter(asset=asset, operation=TransactionOperations.TransactionOperation.BUY)
                            .aggregate(
                                buy_amount=Sum(
                                    'amount', 
                                    default=0, 
                                    output_field=DecimalField(max_digits=30, decimal_places=18)),
                                total_buy_value=Sum(
                                        'total_value', 
                                        default=0, 
                                        output_field=DecimalField(max_digits=12, decimal_places=2)),
                                total_buy_fees=Sum(
                                        'fees', 
                                        default=0,
                                        output_field=DecimalField(max_digits=12, decimal_places=2))
                            ))

            asset_sells = (TransactionOperations.objects
                            .filter(asset=asset, operation=TransactionOperations.TransactionOperation.SELL)
                            .aggregate(
                                sell_amount=Sum(
                                    'amount',
                                    default=0,
                                    output_field=DecimalField(max_digits=30, decimal_places=18)),
                            ))

            institutions = (TransactionOperations.objects
                            .filter(asset=asset)
                            .values_list('institution_name', flat=True)
                            .distinct())

            item = {}
            item['ticker'] = asset.asset_ticker
            item['amount'] = asset_buys['buy_amount'] - asset_sells['sell_amount']
            item['institutions'] = ', '.join(institutions)

            try:
                item['average_buy_price'] = (asset_buys['total_buy_value'] + asset_buys['total_buy_fees'])/asset_buys['buy_amount']
            except InvalidOperation:
                item['average_buy_price'] = 0

            item['total_value'] = item['amount']*item['average_buy_price']
            summary.append(item)

        context['summary'] = summary
        return context


class TransactionDetailView(ListView):
    model = TransactionOperations
    context_object_name = "transactions"
    template_name = "transactions/transaction_detail.html"

    def get_queryset(self):
        ticker = self.kwargs.get('ticker')
        queryset = TransactionOperations.objects.filter(asset__asset_ticker=ticker)

        # Filtering
        filter_operation = self.request.GET.get('filter_operation', '')
        if filter_operation:
            queryset = queryset.filter(operation=filter_operation)

        # Sorting
        sort = self.request.GET.get('sort', '-settlement_date')
        valid_sort_fields = ['settlement_date', '-settlement_date', 'operation', '-operation', 'amount', '-amount', 'total_value', '-total_value']
        if sort in valid_sort_fields:
            queryset = queryset.order_by(sort)
        else:
            queryset = queryset.order_by('-settlement_date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #  context['current_sort'] = self.request.GET.get('sort', '-settlement_date')
        #  context['current_filter_operation'] = self.request.GET.get('filter_operation', '')
        context['ticker'] = self.kwargs.get('ticker')
        return context

