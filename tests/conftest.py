from collections import namedtuple

import pytest
from rest_framework.test import APIClient

User = namedtuple("User", "username")


@pytest.fixture
def user(settings):
    return User(username="user")


@pytest.fixture
def admin_user(settings):
    return User(username="admin")


@pytest.fixture
def client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client
