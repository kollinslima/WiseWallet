import pytest

from .factories import B3TransactionsFileFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from transactions.models import TransactionOperations

@pytest.mark.django_db
def test_transaction_root_upload_success(client):
    ### Arrange ###
    b3_well_formatted_transaction_file = B3TransactionsFileFactory()
    form_data = {
        'file_field': b3_well_formatted_transaction_file
    }

    ### Act ###
    response = client.post(
        path='/transactions/upload',
        data=form_data,
        follow=True
    )

    ### Assert ###
    assert 200 == response.status_code
    assert 'transactions/transactions.html' in response.template_name
    assert 1 <= TransactionOperations.objects.count()

@pytest.mark.django_db
def test_transactions_root_upload_of_non_xlsx_file(client):
    ### Arrange ###
    txt_file = SimpleUploadedFile("test.txt", b'This is a test File', content_type='text/plain')
    form_data = {
        'file_field': txt_file
    }

    ### Act ###
    response = client.post(
        path='/transactions/upload',
        data=form_data,
        follow=True
    )

    ### Assert ###
    assert 200 == response.status_code
    assert 'transactions/transactions_upload.html' in response.template_name
    assert 'Invalid file format. Please upload a .xlsx file.' in response.content.decode('utf-8')
    assert 0 == TransactionOperations.objects.count()

@pytest.mark.django_db
def test_transactions_root_upload_of_corrupted_xlsx_file(client):
    ### Arrange ###
    corrupted_file = SimpleUploadedFile("test.xlsx", b'This is a corrupted test File', content_type='text/plain')
    form_data = {
        'file_field': corrupted_file
    }

    ### Act ###
    response = client.post(
        path='/transactions/upload',
        data=form_data,
        follow=True
    )

    ### Assert ###
    assert 200 == response.status_code
    assert 'transactions/transactions_upload.html' in response.template_name
    assert 'Cannot open XLSX file.' in response.content.decode('utf-8')
    assert 0 == TransactionOperations.objects.count()

