from collections import namedtuple

import pytest
from django.apps import apps
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


@pytest.fixture(autouse=True)
def reset_config_classes(settings):
    """Reset the config classes to clean state after test.

    The config classes need to be reset after running tests that
    use them. Otherwise, unrelated tests may get affected.
    """

    # First, set config to original value
    core_config = apps.get_app_config("generic_permissions")
    core_config.ready()
