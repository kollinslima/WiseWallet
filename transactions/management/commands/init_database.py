from django.core.management.base import BaseCommand
from django.db import transaction
from transactions.models import B3TransactionReports, B3_TRANSACTION_REPORT_UPLOAD_DIR
from pathlib import Path

class Command(BaseCommand):
    help = 'Delete and recreate transactions database from CSV files.'

    def add_arguments(self, parser):
        parser.add_argument('--base_path', type=str, help='The path to the directory containing the CSV files.')

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                base_path = Path(options['base_path'])
                b3_transaction_report_path = base_path.joinpath(B3_TRANSACTION_REPORT_UPLOAD_DIR)

                b3_transaction_report_csv_files = [file for file in b3_transaction_report_path.glob("*.csv") if file.is_file()]

                if not b3_transaction_report_csv_files:
                    self.stdout.write(self.style.ERROR(f'No B3 Transaction Report files found in {base_path}'))
                    return

                self.stdout.write(self.style.SUCCESS(f'Found {len(b3_transaction_report_csv_files)} CSV files in {base_path}'))
                reports_to_create = []
                for file in b3_transaction_report_csv_files:
                    self.stdout.write(self.style.SUCCESS(f'Processing {file.relative_to(base_path)}'))
                    reports_to_create.append(
                        B3TransactionReports(
                            report=str(file.relative_to(base_path)),
                        )
                    )

                if reports_to_create:
                    self.stdout.write(self.style.WARNING('Clearing existing B3TransactionReport data.'))
                    B3TransactionReports.objects.all().delete()
                    B3TransactionReports.objects.bulk_create(reports_to_create)

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))
            return

        self.stdout.write(self.style.SUCCESS('Database has been successfully populated with B3 transactions.'))