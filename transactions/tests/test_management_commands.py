import tempfile

from io import StringIO
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.test import (
    TestCase,
    override_settings
)

from transactions.models import (
    B3TransactionReports, 
    B3_TRANSACTION_REPORT_UPLOAD_DIR
)

from .factories import CsvFactory, B3TransactionReportsFactory

@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class InitDatabaseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._num_csv_files = 5
        cls._base_path = settings.MEDIA_ROOT
        cls._csv_files = CsvFactory.create_batch(
            size=cls._num_csv_files,
            path=Path(cls._base_path).joinpath(B3_TRANSACTION_REPORT_UPLOAD_DIR)
        )

    @classmethod
    def tearDownClass(cls):
        for file in cls._csv_files:
            file.unlink()
        super().tearDownClass()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_from_empty_database(self):
        ### Arrange ###
        B3TransactionReports.objects.all().delete()
        out = StringIO()

        ### Act ###
        call_command("init_database", base_path=self._base_path, stdout=out)

        ### Assert ###
        self.assertEqual(self._num_csv_files, B3TransactionReports.objects.count())
        for report_entry in B3TransactionReports.objects.all():
            report_path = Path(report_entry.report.name)
            full_report_path = Path(settings.MEDIA_ROOT).joinpath(report_path)
            self.assertIn(full_report_path, self._csv_files)

    def test_init_from_non_empty_database(self):
        ### Arrange ###
        out = StringIO()

        # Create initial entries somewhere else
        with self.settings(MEDIA_ROOT=tempfile.mkdtemp()):
            B3TransactionReportsFactory.create_batch(
                size=self._num_csv_files
            )

        ### Act ###
        call_command("init_database", base_path=self._base_path, stdout=out)

        ### Assert ###
        self.assertEqual(self._num_csv_files, B3TransactionReports.objects.count())
        for report_entry in B3TransactionReports.objects.all():
            report_path = Path(report_entry.report.name)
            full_report_path = Path(settings.MEDIA_ROOT).joinpath(report_path)
            self.assertIn(full_report_path, self._csv_files)
