import pytest

@pytest.mark.django_db
def test_transactions_root_page_with_empty_database(client):
    ### Arrange ###

    ### Act ###
    response = client.get(path='/transactions/')

    ### Assert ###
    assert 200 == response.status_code
    assert 'No trades found. Import a report to get started.' in response.content.decode('utf-8')
