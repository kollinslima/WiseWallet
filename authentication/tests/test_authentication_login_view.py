import pytest
import re

from django.urls import reverse
from tests.fixtures import logged_user

def test_login_page_endpoint(client):
    ### Arrange ###

    ### Act ###
    response = client.get(path=reverse('authentication:index'))

    ### Assert ###
    assert 200 == response.status_code
    assert 'authentication/login.html' in response.template_name

def test_login_page_signup_link_is_present(client):
    ### Arrange ###

    ### Act ###
    response = client.get(path=reverse('authentication:index'))

    ### Assert ###
    assert 200 == response.status_code
    assert re.search(r'<a\s+href=["\']{}["\']'.format(reverse('authentication:index.signup')), response.content.decode('utf-8'))


@pytest.mark.django_db
def test_login_page_authenticated_user_is_redirected_to_dashboard(client, logged_user):
    ### Arrange ###

    ### Act ###
    response = client.get(path=reverse('authentication:index'), follow=True)

    ### Assert ###
    assert 200 == response.status_code
    assert 'dashboard/dashboard.html' in response.template_name

def test_signup_page_endpoint(client):
    ### Arrange ###

    ### Act ###
    response = client.get(path=reverse('authentication:index.signup'))

    ### Assert ###
    assert 200 == response.status_code
    assert 'authentication/signup.html' in response.template_name

@pytest.mark.django_db
def test_signup_page_authenticated_user_is_redirected_to_dashboard(client, logged_user):
    ### Arrange ###

    ### Act ###
    response = client.get(path=reverse('authentication:index.signup'), follow=True)

    ### Assert ###
    assert 200 == response.status_code
    assert 'dashboard/dashboard.html' in response.template_name

