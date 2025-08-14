import pytest
from .factories import UserFactory

@pytest.fixture
def logged_user(client):
    """
    Create logged user for tests.
    """
    user = UserFactory()
    client.login(username=user.username, password="password")
    return user
