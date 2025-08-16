from django.db import models, transaction
from django.core.files.storage import FileSystemStorage
from django.utils.text import get_valid_filename
from pathlib import Path

B3_TRANSACTION_REPORT_UPLOAD_DIR = Path('reports/B3/transactions/')

class B3TransactionReports(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['report'], name='unique_b3_transaction_report')
        ]
    report = models.FileField(upload_to=str(B3_TRANSACTION_REPORT_UPLOAD_DIR), 
                              storage=FileSystemStorage(allow_overwrite=True))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            valid_name = get_valid_filename(self.report.name)
            existing_record = B3TransactionReports.objects.select_for_update().filter(
                report=B3_TRANSACTION_REPORT_UPLOAD_DIR.joinpath(Path(valid_name))
            ).first()

            if existing_record:
                # Update existing record
                self.pk = existing_record.pk
                self.created_at = existing_record.created_at

            super(B3TransactionReports, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.updated_at.strftime('%Y-%m-%d %H:%M:%S')} - {self.report.name}"