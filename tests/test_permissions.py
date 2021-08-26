import pytest
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
)

from generic_permissions.config import ObjectPermissionsConfig, PermissionsConfig
from generic_permissions.permissions import (
    DenyAll,
    object_permission_for,
    permission_for,
)
from tests.views import Test1ViewSet, Test2ViewSet

from .models import Model1, Model2


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
):
    client = admin_client if use_admin_client else client

    class CustomPermission:
        @permission_for(Model1)
        def has_permission_for_document(self, request):
            if (
                hasattr(request, "user")
                and request.user.username == "admin"
                or request.data["text"] == "baz"
            ):
                return True
            return False

        @object_permission_for(Model1)
        def has_object_permission_for_document(self, request, instance):
            assert isinstance(instance, Model1)
            if hasattr(request, "user") and request.user.username == "admin":
                return True
            return False

    PermissionsConfig.register_handler_class(CustomPermission)
    ObjectPermissionsConfig.register_handler_class(CustomPermission)

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


def test_custom_permission_override_has_permission_with_duplicates():
    class CustomPermission:
        @permission_for(Model1)
        def has_permission_for_custom_mutation(self, request):  # pragma: no cover
            return False

        @permission_for(Model1)
        def has_permission_for_custom_mutation_2(self, request):  # pragma: no cover
            return False

    with pytest.raises(ImproperlyConfigured):
        PermissionsConfig.register_handler_class(CustomPermission)


def test_custom_permission_override_has_object_permission_with_duplicates():
    class CustomPermission:
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
        ObjectPermissionsConfig.register_handler_class(CustomPermission)


def test_custom_permission_override_has_permission_with_multiple_models(admin_client):
    class CustomPermission:
        @permission_for(Model1)
        @permission_for(Model2)
        def has_permission_for_both_mutations(self, request):
            return False

    PermissionsConfig.register_handler_class(CustomPermission)

    for model in Model1, Model2:
        url = reverse(f"{model.__name__.lower()}-list")
        resp = admin_client.post(url, data={"text": "foo"}, format="json")
        assert resp.status_code == HTTP_403_FORBIDDEN


def test_custom_permission_override_has_object_permission_with_multiple_mutations(
    db, admin_client
):
    class CustomPermission:
        @object_permission_for(Model1)
        def has_object_permission_for_both_mutations(self, request, instance):
            return False

    ObjectPermissionsConfig.register_handler_class(CustomPermission)

    tm1 = Model1.objects.create()

    url = reverse("model1-detail", args=[tm1.pk])
    resp = admin_client.patch(url, data={"text": "foo"}, format="json")
    assert resp.status_code == HTTP_403_FORBIDDEN


def test_custom_permission_fallback_to_true(
    db,
    rf,
):
    class CustomPermission:
        @permission_for(Model2)
        def has_permission_for_document(self, request):  # pragma: no cover
            return False

        @object_permission_for(Model2)
        def has_object_permission_for_both_mutations(
            self, request, instance
        ):  # pragma: no cover
            return False

    tm1 = Model1.objects.create()
    ObjectPermissionsConfig.register_handler_class(CustomPermission)
    PermissionsConfig.register_handler_class(CustomPermission)

    request = rf.patch("")
    request.data = {"text": "foo"}

    Test1ViewSet(request=request, format_kwarg="json")._check_permissions(request)
    Test1ViewSet(request=request, format_kwarg="json").check_object_permissions(
        request, tm1
    )


def test_deny_all_permission(
    db,
    rf,
):
    class CustomPermission(DenyAll):
        @permission_for(Model2)
        def has_permission_for_document(self, request):
            return True

        @object_permission_for(Model2)
        def has_object_permission_for_both_mutations(self, request, instance):
            return True

    tm1 = Model1.objects.create()
    tm2 = Model2.objects.create()
    ObjectPermissionsConfig.register_handler_class(CustomPermission)
    PermissionsConfig.register_handler_class(CustomPermission)

    request = rf.patch("")
    request.data = {"text": "foo"}

    # Model2 access should be granted by above permission class
    Test2ViewSet(request=request, format_kwarg="json")._check_permissions(request)
    Test2ViewSet(request=request, format_kwarg="json").check_object_permissions(
        request, tm2
    )

    # Model1 access should "bubble up" to the DenyAll base class and be denied
    with pytest.raises(PermissionDenied):
        Test1ViewSet(request=request, format_kwarg="json")._check_permissions(request)

    with pytest.raises(PermissionDenied):
        Test1ViewSet(request=request, format_kwarg="json").check_object_permissions(
            request, tm1
        )
