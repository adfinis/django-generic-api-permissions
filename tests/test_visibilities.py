import pytest
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from generic_permissions.visibilities import BaseVisibility, Union, filter_queryset_for

from .models import BaseModel, Model1, Model2, VisibilityModelMixin


@pytest.fixture
def reset_visibilities():
    before = VisibilityModelMixin.visibility_classes
    yield
    VisibilityModelMixin.visibility_classes = before


@pytest.mark.parametrize("detail", [True, False])
@pytest.mark.parametrize("use_admin_client", [True, False])
def test_visibility(
    db,
    reset_visibilities,
    admin_user,
    admin_client,
    client,
    detail,
    use_admin_client,
):
    client = admin_client if use_admin_client else client

    class TestVisibility(BaseVisibility):
        @filter_queryset_for(Model1)
        def filter_queryset_for_document(self, queryset, request):
            if request.user.username != "admin":
                return queryset.none()
            return queryset.exclude(text="bar")

    VisibilityModelMixin.visibility_classes = [TestVisibility]

    model1 = Model1.objects.create(text="foo")
    Model1.objects.create(text="bar")

    url = reverse("model1-list")
    if detail:
        url = reverse("model1-detail", args=[model1.pk])
    response = client.get(url)
    if detail and not use_admin_client:
        assert response.status_code == HTTP_404_NOT_FOUND
        return
    assert response.status_code == HTTP_200_OK
    result = response.json()
    if not detail:
        if use_admin_client:
            assert len(result) == 1
            assert result[0]["text"] == "foo"
        else:
            assert len(result) == 0
    else:
        assert result["text"] == "foo"


def test_visibility_no_visibilities_configured(reset_visibilities, client):
    VisibilityModelMixin.visibility_classes = None

    url = reverse("model1-list")
    with pytest.raises(ImproperlyConfigured):
        client.get(url)


def test_visibility_dupes(reset_visibilities, client):
    class TestVisibility(BaseVisibility):
        @filter_queryset_for(Model1)
        def filter_queryset_for_document(self, queryset, request):  # pragma: no cover
            return queryset

        @filter_queryset_for(Model1)
        def filter_queryset_for_document2(self, queryset, request):  # pragma: no cover
            return queryset

    VisibilityModelMixin.visibility_classes = [TestVisibility]

    url = reverse("model1-list")
    with pytest.raises(ImproperlyConfigured):
        client.get(url)


def test_custom_visibility_for_basemodel(reset_visibilities, db, client):
    """Test fallback to BaseModel."""
    Model1.objects.create(text="m1")
    Model1.objects.create(text="m2")

    class CustomVisibility(BaseVisibility):
        @filter_queryset_for(BaseModel)
        def filter_queryset_for_all(self, queryset, request):
            return queryset.none()

    VisibilityModelMixin.visibility_classes = [CustomVisibility]

    assert Model1.objects.count() == 2

    url = reverse("model1-list")
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    result = response.json()

    assert result == []


def test_custom_visibility_override_specificity(db):
    """The first matching filter 'wins'."""
    Model1.objects.create(text="m1")
    Model1.objects.create(text="m2")

    class CustomVisibility(BaseVisibility):
        @filter_queryset_for(BaseModel)
        def filter_queryset_for_all(self, queryset, request):
            return queryset.none()

        @filter_queryset_for(Model1)
        def filter_queryset_for_document(self, queryset, request):
            return queryset.filter(text="m1")

    assert Model1.objects.count() == 2
    queryset = CustomVisibility().filter_queryset(BaseModel, Model1.objects, None)
    assert queryset.count() == 0
    queryset = CustomVisibility().filter_queryset(Model1, Model1.objects, None)
    assert queryset.count() == 1


def test_custom_visibility_chained_decorators(db):
    class CustomVisibility(BaseVisibility):
        @filter_queryset_for(BaseModel)
        def filter_queryset_for_all(self, queryset, request):
            return queryset.none()

        @filter_queryset_for(Model1)
        @filter_queryset_for(Model2)
        def filter_queryset_for_custom_node(self, queryset, request):
            return queryset.filter(text="name1")

    Model1.objects.create(text="name1")
    Model1.objects.create(text="name2")
    Model2.objects.create(text="name1")
    Model2.objects.create(text="name2")

    assert Model1.objects.count() == 2
    assert Model2.objects.count() == 2
    queryset = CustomVisibility().filter_queryset(BaseModel, Model1.objects, None)
    assert queryset.count() == 0
    queryset = CustomVisibility().filter_queryset(Model1, Model1.objects, None)
    assert queryset.count() == 1
    queryset = CustomVisibility().filter_queryset(Model2, Model2.objects, None)
    assert queryset.count() == 1


def test_union_visibility(db):
    Model1.objects.create(text="m1")
    Model1.objects.create(text="m2")
    Model1.objects.create(text="m3")
    Model1.objects.create(text="m4")

    class Name1Visibility(BaseVisibility):
        @filter_queryset_for(Model1)
        def filter_queryset_for_custom_node(self, queryset, request):
            return queryset.filter(text="m1")

    class Name2Visibility(BaseVisibility):
        @filter_queryset_for(Model1)
        def filter_queryset_for_custom_node(self, queryset, request):
            return queryset.filter(text="m2")

    class Name3Visibility(BaseVisibility):
        @filter_queryset_for(Model1)
        def filter_queryset_for_custom_node(self, queryset, request):
            return queryset.filter(text__in=["m2", "m3"])

    class ConfiguredUnion(Union):
        visibility_classes = [Name1Visibility, Name2Visibility, Name3Visibility]

    queryset = Model1.objects
    result = Name1Visibility().filter_queryset(Model1, queryset, None)
    assert result.count() == 1
    result = Name2Visibility().filter_queryset(Model1, queryset, None)
    assert result.count() == 1
    result = Name3Visibility().filter_queryset(Model1, queryset, None)
    assert result.count() == 2
    queryset = ConfiguredUnion().filter_queryset(Model1, queryset, None)
    assert queryset.count() == 3
    assert queryset.get(text="m2")


def test_union_visibility_none(db):
    Model1.objects.create(text="m1")

    class CustomVisibility(BaseVisibility):
        @filter_queryset_for(Model1)
        def filter_queryset_for_custom_node(self, queryset, request):
            return queryset.none()

    class CustomVisibility2(BaseVisibility):
        @filter_queryset_for(Model1)
        def filter_queryset_for_custom_node(self, queryset, request):
            return queryset.none()

    class ConfiguredUnion(Union):
        visibility_classes = [CustomVisibility2, CustomVisibility]

    queryset = Model1.objects
    result = CustomVisibility().filter_queryset(Model1, queryset, None)
    assert result.count() == 0
    result = CustomVisibility2().filter_queryset(Model1, queryset, None)
    assert result.count() == 0
    queryset = ConfiguredUnion().filter_queryset(Model1, queryset, None)
    assert queryset.count() == 0
