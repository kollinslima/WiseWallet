from .forms import TransactionsFileUploadForm
from django.views.generic.edit import FormView
from django.views.generic import TemplateView

class TransactionsFileUploadFormView(FormView):
    form_class = TransactionsFileUploadForm
    template_name = "transactions/transactions.html"
    success_url = "upload/success"

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]
        for f in files:
            print(f)
        return super().form_valid(form)

class TransactionsFileUploadSuccessView(TemplateView):
    template_name = "transactions/transactions_upload_success.html"

