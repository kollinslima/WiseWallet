from .forms import TransactionsFileUploadForm
from .services import process_transactions_file
from django.core.exceptions import ValidationError
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

class TransactionsFileUploadFormView(FormView):
    form_class = TransactionsFileUploadForm
    template_name = "transactions/transactions.html"
    success_url = "upload/success"

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

