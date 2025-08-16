
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic import TemplateView

import logging

logger = logging.getLogger(__name__)

class TransactionsView(LoginRequiredMixin, TemplateView):
    template_name = "transactions/transactions.html"

class TransactionDetailView(LoginRequiredMixin, ListView):
    context_object_name = "transactions"
    template_name = "transactions/transaction_detail.html"



