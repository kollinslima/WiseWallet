import factory
from factory import fuzzy
from django.contrib.auth.models import User 
from django.contrib.auth.hashers import make_password

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"testuser_{n:04}") # user_0001, user_0002, etc.
    email = factory.LazyAttribute(lambda user: f"{user.username}@unittest.com")
    password = factory.LazyFunction(lambda: make_password("password")) 

