import pytest
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
)

from generic_permissions.models import PermissionModelMixin
from generic_permissions.permissions import (
    BasePermission,
    object_permission_for,
    permission_for,
)

from .models import Model1, Model2


@pytest.fixture
def reset_permission_classes():
    before = PermissionModelMixin.permission_classes
    yield
    PermissionModelMixin.permission_classes = before


@pytest.mark.parametrize(
    "method,status",
    [
        ("post", HTTP_201_CREATED),
        ("patch", HTTP_200_OK),
        ("delete", HTTP_204_NO_CONTENT),
    ],
)
@pytest.mark.parametrize("use_admin_client", [True, False])
def test_permission(
    db,
    admin_client,
    client,
    method,
    status,
    use_admin_client,
    reset_permission_classes,
):
    client = admin_client if use_admin_client else client

    class CustomPermission(BasePermission):
        @permission_for(Model1)
        def has_permission_for_document(self, request):
            if request.user.username == "admin" or request.data["text"] == "baz":
                return True
            return False

        @object_permission_for(Model1)
        def has_object_permission_for_document(self, request, instance):
            assert isinstance(instance, Model1)
            if request.user.username == "admin":
                return True
            return False

    PermissionModelMixin.permission_classes = [CustomPermission]

    tm = Model1.objects.create(text="foo")

    url = reverse("model1-list")

    if method in ["patch", "delete"]:
        url = reverse("model1-detail", args=[tm.pk])

    data = {"text": "bar"}
    if method == "patch":
        data = {"text": "baz"}

    response = getattr(client, method)(url, data=data)

    if not use_admin_client:
        assert response.status_code == HTTP_403_FORBIDDEN
        return

    assert response.status_code == status

    if method == "post":
        assert response.json()["text"] == "bar"
        Model1.objects.get(text="bar")
    elif method == "patch":
        assert response.json()["text"] == "baz"
        tm.refresh_from_db()
        assert tm.text == "baz"


def test_permission_no_permissions_configured(client, reset_permission_classes):
    PermissionModelMixin.permission_classes = None

    data = {"text": "foo"}

    url = reverse("model1-list")
    with pytest.raises(ImproperlyConfigured):
        client.post(url, data=data)


def test_custom_permission_override_has_permission_with_duplicates():
    class CustomPermission(BasePermission):
        @permission_for(Model1)
        def has_permission_for_custom_mutation(self, request):  # pragma: no cover
            return False

        @permission_for(Model1)
        def has_permission_for_custom_mutation_2(self, request):  # pragma: no cover
            return False

    with pytest.raises(ImproperlyConfigured):
        CustomPermission()


def test_custom_permission_override_has_object_permission_with_duplicates():
    class CustomPermission(BasePermission):
        @object_permission_for(Model1)
        def has_object_permission_for_custom_mutation(
            self, request, instance
        ):  # pragma: no cover
            return False

        @object_permission_for(Model1)
        def has_object_permission_for_custom_mutation_2(
            self, request, instance
        ):  # pragma: no cover
            return False

    with pytest.raises(ImproperlyConfigured):
        CustomPermission()


def test_custom_permission_override_has_permission_with_multiple_models(request):
    class CustomPermission(BasePermission):
        @permission_for(Model1)
        @permission_for(Model2)
        def has_permission_for_both_mutations(self, request):  # pragma: no cover
            return False

    assert not CustomPermission().has_permission(Model1, request)
    assert not CustomPermission().has_permission(Model2, request)


def test_custom_permission_override_has_object_permission_with_multiple_mutations(
    db, request
):
    class CustomPermission(BasePermission):
        @object_permission_for(Model1)
        @object_permission_for(Model2)
        def has_object_permission_for_both_mutations(
            self, request, instance
        ):  # pragma: no cover
            return False

    tm1 = Model1.objects.create()
    tm2 = Model1.objects.create()

    assert not CustomPermission().has_object_permission(Model1, request, tm1)
    assert not CustomPermission().has_object_permission(Model2, request, tm2)


def test_custom_permission_fallback_to_true(db, request):
    class CustomPermission(BasePermission):
        @permission_for(Model2)
        def has_permission_for_document(self, request):  # pragma: no cover
            return False

        @object_permission_for(Model2)
        def has_object_permission_for_both_mutations(
            self, request, instance
        ):  # pragma: no cover
            return False

    tm1 = Model1.objects.create()

    assert CustomPermission().has_permission(Model1, request)
    assert CustomPermission().has_object_permission(Model1, request, tm1)
