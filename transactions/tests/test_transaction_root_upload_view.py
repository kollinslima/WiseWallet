import pytest

from .factories import B3TransactionsFileFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from transactions.models import TransactionOperations
from django.urls import reverse

@pytest.mark.django_db
def test_transaction_index_upload_success(client):
    ### Arrange ###
    b3_well_formatted_transaction_file = B3TransactionsFileFactory()
    form_data = {
        'file_field': b3_well_formatted_transaction_file
    }

    ### Act ###
    response = client.post(
        path=reverse('transactions:index.upload'),
        data=form_data,
        follow=True
    )

    ### Assert ###
    assert 200 == response.status_code
    assert 'transactions/transactions.html' in response.template_name
    assert 1 <= TransactionOperations.objects.count()

@pytest.mark.django_db
def test_transactions_index_upload_of_non_xlsx_file(client):
    ### Arrange ###
    txt_file = SimpleUploadedFile("test.txt", b'This is a test File', content_type='text/plain')
    form_data = {
        'file_field': txt_file
    }

    ### Act ###
    response = client.post(
        path=reverse('transactions:index.upload'),
        data=form_data,
        follow=True
    )

    ### Assert ###
    assert 200 == response.status_code
    assert 'transactions/transactions_upload.html' in response.template_name
    assert 'Invalid file format. Please upload a .xlsx file.' in response.content.decode('utf-8')
    assert 0 == TransactionOperations.objects.count()

@pytest.mark.django_db
def test_transactions_index_upload_of_corrupted_xlsx_file(client):
    ### Arrange ###
    corrupted_file = SimpleUploadedFile("test.xlsx", b'This is a corrupted test File', content_type='text/plain')
    form_data = {
        'file_field': corrupted_file
    }

    ### Act ###
    response = client.post(
        path=reverse('transactions:index.upload'),
        data=form_data,
        follow=True
    )

    ### Assert ###
    assert 200 == response.status_code
    assert 'transactions/transactions_upload.html' in response.template_name
    assert 'Cannot open XLSX file.' in response.content.decode('utf-8')
    assert 0 == TransactionOperations.objects.count()

@pytest.mark.django_db
def test_transactions_index_upload_of_incomplete_xlsx_file(client):
    b3_incomplete_transaction_file = B3TransactionsFileFactory(
        header=["Date", "Transaction", "Ticker", "Amount", "Total Value"],
        num_of_transactions=1
    )
    form_data = {
        'file_field': b3_incomplete_transaction_file
    }

    ### Act ###
    response = client.post(
        path=reverse('transactions:index.upload'),
        data=form_data,
        follow=True
    )

    ### Assert ###
    assert 200 == response.status_code
    assert 'transactions/transactions_upload.html' in response.template_name
    assert "Invalid data in row" in response.content.decode('utf-8')
    assert "Error: &lt;B3TransactionsReportHeader.IN_OUT_TRANSACTION_TYPE: &#x27;Entrada/Saída&#x27;&gt;" in response.content.decode('utf-8')
    assert 0 == TransactionOperations.objects.count()

@pytest.mark.django_db
@pytest.mark.parametrize("field,value", [
    ("Data", "INVALID"),
    ("Produto", "INVALID"),
    ("Quantidade", "INVALID"),
    ("Valor da Operação", "INVALID"),
])
def test_transactions_index_upload_of_invalid_xlsx_file(client, field, value):
    ### Arrange ###
    content = [["Credito", "01/01/2024", "Transferência - Liquidação", "TICKER11 - NAME", "INSTITUTION", 100, "R$ 10,00", "R$ 1.000,00"]]
    
    header = ["Entrada/Saída", "Data", "Movimentação", "Produto", "Instituição", "Quantidade", "Preço unitário", "Valor da Operação"]
    field_index = header.index(field)
    
    content[0][field_index] = value
    
    b3_invalid_transaction_file = B3TransactionsFileFactory(
        content=content,
    )
    
    form_data = {
        'file_field': b3_invalid_transaction_file
    }

    ### Act ###
    response = client.post(
        path=reverse('transactions:index.upload'),
        data=form_data,
        follow=True
    )

    ### Assert ###
    assert 200 == response.status_code
    assert 'transactions/transactions_upload.html' in response.template_name
    assert "Invalid data in row" in response.content.decode('utf-8')
    assert 0 == TransactionOperations.objects.count()
