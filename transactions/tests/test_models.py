import tempfile
import time
import os

from io import StringIO
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.files.base import ContentFile
from django.test import (
    TestCase,
    TransactionTestCase,
    override_settings
)

from transactions.models import (
    B3TransactionReports, 
    B3_TRANSACTION_REPORT_UPLOAD_DIR
)

from .factories import B3TransactionReportsFactory

class B3TransactionModelsTest(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._num_csv_files = 5

    def setUp(self):
        B3TransactionReports.objects.all().delete()

    def tearDown(self):
        pass

    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_files_are_uploaded_to_filetystem(self):
        ### Arrange ###

        ### Act ###
        B3TransactionReportsFactory.create_batch(
            size=self._num_csv_files
        )

        ### Assert ###
        self.assertEqual(self._num_csv_files, B3TransactionReports.objects.count())
        for report_entry in B3TransactionReports.objects.all():
            report_path = Path(report_entry.report.name)
            full_report_path = Path(settings.MEDIA_ROOT).joinpath(report_path)
            self.assertTrue(full_report_path.exists())


    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_files_are_updated_in_filesystem_if_reuploaded(self):
        ### Arrange ###
        B3TransactionReportsFactory.create_batch(
            size=self._num_csv_files
        )
        initial_reports = list(B3TransactionReports.objects.all())
        initial_creation_time = {}
        initial_update_time = {}
        initial_file_stats = {}
        for report_entry in initial_reports:
            report_path = Path(report_entry.report.name)
            full_reports_path = Path(settings.MEDIA_ROOT).joinpath(report_path)

            initial_creation_time[report_entry.pk] = report_entry.created_at
            initial_update_time[report_entry.pk] = report_entry.updated_at
            initial_file_stats[report_entry.pk] = full_reports_path.stat()
            
        ### Act ###
        time.sleep(1)
        for report_entry in initial_reports:
            original_filename = Path(report_entry.report.name).name
            updated_report = ContentFile(b"", name=original_filename)
            report_entry.report = updated_report
            report_entry.save()

        ### Assert ###
        self.assertEqual(self._num_csv_files, B3TransactionReports.objects.count())
        for report_entry in B3TransactionReports.objects.all():
            report_path = Path(report_entry.report.name)
            full_reports_path = Path(settings.MEDIA_ROOT).joinpath(report_path)

            self.assertEqual(report_entry.created_at, initial_creation_time[report_entry.pk])
            self.assertGreater(report_entry.updated_at, initial_update_time[report_entry.pk])

            # Make sure files was actually updated in the filesystem
            self.assertGreater(full_reports_path.stat().st_mtime, initial_file_stats[report_entry.pk].st_mtime)

    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_uploaded_files_are_removed_from_filesystem_on_database_delete(self):
        ### Arrange ###
        B3TransactionReportsFactory.create_batch(
            size=self._num_csv_files
        )
        full_reports_path = []
        for report_entry in B3TransactionReports.objects.all():
            report_path = Path(report_entry.report.name)
            full_reports_path.append(Path(settings.MEDIA_ROOT).joinpath(report_path))

        ### Act ###
        B3TransactionReports.objects.all().delete()

        ### Assert ###
        self.assertEqual(0, B3TransactionReports.objects.count())
        for report_path in full_reports_path:
            self.assertFalse(report_path.exists())