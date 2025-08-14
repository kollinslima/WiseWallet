import pytest

from .factories import TransactionOperationFactory, AssetIdentificationFactory
from decimal import Decimal, InvalidOperation, ROUND_DOWN
from transactions.models import TransactionOperations
from django.urls import reverse

@pytest.mark.django_db
def test_transactions_index_page_with_empty_database(client):
    ### Arrange ###

    ### Act ###
    response = client.get(path=reverse('transactions:index'))

    ### Assert ###
    assert 200 == response.status_code
    assert 'No trades found. Import a report to get started.' in response.content.decode('utf-8')

@pytest.mark.django_db
@pytest.mark.parametrize("num_transactions", [1,10])
def test_transactions_index_page_distinct_assets(client, num_transactions):
    ### Arrange ###
    transactions = TransactionOperationFactory.create_batch(size=num_transactions)

    ### Act ###
    response = client.get(path=reverse('transactions:index'))

    ### Assert ###
    assert 200 == response.status_code
    assert 'transactions/transactions.html' in response.template_name
    
    summary = response.context['summary']
    assert num_transactions == len(summary)
    
    for transaction in transactions:
        assert transaction.asset.asset_ticker in [item["ticker"] for item in summary]
        assert transaction.institution_name.institution_name in [item["institutions"] for item in summary]

@pytest.mark.django_db
@pytest.mark.parametrize("num_transactions", [1,10])
def test_transactions_index_page_same_assets(client, num_transactions):
    ### Arrange ###
    fixed_asset = AssetIdentificationFactory.create()
    transactions = TransactionOperationFactory.create_batch(size=num_transactions, asset=fixed_asset, operation=TransactionOperations.TransactionOperation.BUY)

    ### Act ###
    response = client.get(path=reverse('transactions:index'))

    ### Assert ###
    assert 200 == response.status_code
    assert 'transactions/transactions.html' in response.template_name
    
    summary = response.context['summary']
    assert 1 == len(summary)
    
    assert fixed_asset.asset_ticker == summary[0]["ticker"]

    total_amount = sum(transaction.amount for transaction in transactions)
    assert total_amount == summary[0]["amount"]

    total_buy_price = sum(transaction.total_value + transaction.fees for transaction in transactions)
    assert total_buy_price == pytest.approx(summary[0]["total_value"], abs=1e-2)

    average_buy_price = total_buy_price/total_amount
    assert average_buy_price == pytest.approx(summary[0]["average_buy_price"], abs=1e-2)

    for transaction in transactions:
        assert transaction.institution_name.institution_name in summary[0]["institutions"]
