import pytest

from .factories import TransactionOperationFactory, AssetIdentificationFactory
from decimal import Decimal, InvalidOperation, ROUND_DOWN
from transactions.models import TransactionOperations
from django.urls import reverse
from tests.fixtures import logged_user
from tests.factories import UserFactory

def test_transactions_index_detail_page_redirects_to_login_for_unauthenticated_users(client):
    ### Arrange ###

    ### Act ###
    response = client.get(
        path=reverse('transactions:index.detail', 
        kwargs={'ticker':'TICKER'}), 
        follow=True)

    ### Assert ###
    assert 200 == response.status_code
    assert 'authentication/login.html' in response.template_name
    
@pytest.mark.django_db
@pytest.mark.parametrize("num_transactions", [1,10])
def test_transactions_index_detail_page_list_all_transactions_for_asset(client, num_transactions, logged_user):
    ### Arrange ###
    fixed_asset = AssetIdentificationFactory.create(user=logged_user)
    transactions = TransactionOperationFactory.create_batch(
        size=num_transactions, 
        user=logged_user, 
        asset=fixed_asset, 
        operation=TransactionOperations.TransactionOperation.BUY)

    ### Act ###
    response = client.get(
        path=reverse('transactions:index.detail',
        kwargs={'ticker': fixed_asset.name}))

    ### Assert ###
    assert 200 == response.status_code
    assert 'transactions/transaction_detail.html' in response.template_name
    assert f"Transactions for {fixed_asset.name}" in response.content.decode("utf-8")

# TODO: Add tests for sort and filter functionality
