import pytest
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from generic_permissions.config import VisibilitiesConfig
from generic_permissions.visibilities import (
    Union,
    VisibilityPrimaryKeyRelatedField,
    filter_queryset_for,
)

from .models import BaseModel, Model1, Model2


@pytest.mark.parametrize("has_qs", [True, False])
@pytest.mark.parametrize("detail", [True, False])
@pytest.mark.parametrize("use_admin_client", [True, False])
def test_visibility(
    db,
    admin_user,
    admin_client,
    client,
    detail,
    use_admin_client,
    has_qs,
    mocker,
):
    client = admin_client if use_admin_client else client

    class TestVisibility:
        @filter_queryset_for(Model1)
        def filter_queryset_for_document(self, queryset, request):
            return self.visibility(queryset, request)

        @classmethod
        def visibility(cls, queryset, request):
            assert isinstance(request, Request)
            if request.user.username != "admin":
                return queryset.none()
            return queryset.exclude(text="bar")

    spy = mocker.spy(TestVisibility, "visibility")

    VisibilitiesConfig.register_handler_class(TestVisibility)

    if has_qs:
        model1_id = Model1.objects.create(text="foo").pk
        Model1.objects.create(text="bar")
    else:
        model1_id = 1

    url = reverse("model1-list")
    if detail:
        url = reverse("model1-detail", args=[model1_id])
    response = client.get(url)

    if has_qs:
        assert spy.call_count == 1
    else:
        assert spy.call_count == 0

    if detail and (not use_admin_client or not has_qs):
        assert response.status_code == HTTP_404_NOT_FOUND
        return

    assert response.status_code == HTTP_200_OK
    result = response.json()

    if not detail:
        if use_admin_client and has_qs:
            assert len(result) == 1
            assert result[0]["text"] == "foo"
        else:
            assert len(result) == 0
    else:
        assert result["text"] == "foo"


def test_visibility_dupes(client):
    class TestVisibility:
        @filter_queryset_for(Model1)
        def filter_queryset_for_document(self, queryset, request):  # pragma: no cover
            return queryset

        @filter_queryset_for(Model1)
        def filter_queryset_for_document2(self, queryset, request):  # pragma: no cover
            return queryset

    with pytest.raises(ImproperlyConfigured):
        VisibilitiesConfig.register_handler_class(TestVisibility)


def test_custom_visibility_for_basemodel(db, client):
    """Test fallback to BaseModel."""
    Model1.objects.create(text="m1")
    Model1.objects.create(text="m2")

    class CustomVisibility:
        @filter_queryset_for(BaseModel)
        def filter_queryset_for_all(self, queryset, request):
            return queryset.none()

    VisibilitiesConfig.register_handler_class(CustomVisibility)

    assert Model1.objects.count() == 2

    url = reverse("model1-list")
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    result = response.json()

    assert result == []


def test_custom_visibility_override_specificity(db, admin_client):
    """The first matching filter 'wins'."""
    Model1.objects.create(text="m1")
    Model1.objects.create(text="m2")

    class CustomVisibility:
        @filter_queryset_for(BaseModel)
        def filter_queryset_for_all(self, queryset, request):
            return queryset.none()  # pragma: no cover

        @filter_queryset_for(Model1)
        def filter_queryset_for_document(self, queryset, request):
            return queryset.filter(text="m1")

    assert Model1.objects.count() == 2

    VisibilitiesConfig.clear_handlers()
    VisibilitiesConfig.register_handler_class(CustomVisibility)

    assert len(admin_client.get(reverse("model1-list")).json()) == 1


def test_custom_visibility_chained_decorators(admin_client, db):
    class CustomVisibility:
        @filter_queryset_for(BaseModel)
        def filter_queryset_for_all(self, queryset, request):
            return queryset.none()  # pragma: no cover

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

    VisibilitiesConfig.clear_handlers()
    VisibilitiesConfig.register_handler_class(CustomVisibility)

    assert len(admin_client.get(reverse("model1-list")).json()) == 1
    assert len(admin_client.get(reverse("model2-list")).json()) == 1


def test_union_visibility(db, admin_client):
    Model1.objects.create(text="m1")
    Model1.objects.create(text="m2")
    Model1.objects.create(text="m3")
    Model1.objects.create(text="m4")

    class Name1Visibility:
        @filter_queryset_for(Model1)
        def filter_queryset_for_custom_node(self, queryset, request):
            return queryset.filter(text="m1")

    class Name2Visibility:
        @filter_queryset_for(Model1)
        def filter_queryset_for_custom_node(self, queryset, request):
            return queryset.filter(text="m2")

    class Name3Visibility:
        @filter_queryset_for(Model1)
        def filter_queryset_for_custom_node(self, queryset, request):
            return queryset.filter(text__in=["m2", "m3"])

    class ConfiguredUnion(Union):
        visibility_classes = [Name1Visibility, Name2Visibility, Name3Visibility]

    url = reverse("model1-list")

    VisibilitiesConfig.clear_handlers()
    VisibilitiesConfig.register_handler_class(Name1Visibility)
    assert len(admin_client.get(url).json()) == 1

    VisibilitiesConfig.clear_handlers()
    VisibilitiesConfig.register_handler_class(Name2Visibility)
    assert len(admin_client.get(url).json()) == 1

    VisibilitiesConfig.clear_handlers()
    VisibilitiesConfig.register_handler_class(Name3Visibility)
    assert len(admin_client.get(url).json()) == 2

    VisibilitiesConfig.clear_handlers()
    VisibilitiesConfig.register_handler_class(ConfiguredUnion)
    assert len(admin_client.get(url).json()) == 3


def test_union_visibility_none(db, admin_client):
    Model1.objects.create(text="m1")

    class CustomVisibility:
        @filter_queryset_for(Model1)
        def filter_queryset_for_custom_node(self, queryset, request):
            return queryset.none()

    class CustomVisibility2:
        @filter_queryset_for(Model1)
        def filter_queryset_for_custom_node(self, queryset, request):
            return queryset.none()

    class ConfiguredUnion(Union):
        visibility_classes = [CustomVisibility2, CustomVisibility]

    url = reverse("model1-list")

    VisibilitiesConfig.clear_handlers()
    VisibilitiesConfig.register_handler_class(CustomVisibility)
    assert len(admin_client.get(url).json()) == 0

    VisibilitiesConfig.clear_handlers()
    VisibilitiesConfig.register_handler_class(CustomVisibility2)
    assert len(admin_client.get(url).json()) == 0

    VisibilitiesConfig.clear_handlers()
    VisibilitiesConfig.register_handler_class(ConfiguredUnion)
    assert len(admin_client.get(url).json()) == 0


@pytest.mark.parametrize("has_qs", [True, False])
@pytest.mark.parametrize("filter_relation", [True, False])
def test_visibility_relation(
    db, admin_user, admin_client, filter_relation, has_qs, mocker
):
    class TestVisibility:
        @filter_queryset_for(Model2)
        def filter_queryset_for_document(self, queryset, request):
            return self.visibility(queryset, request)

        @classmethod
        def visibility(cls, queryset, request):
            assert isinstance(request, Request)
            if filter_relation:
                return queryset.exclude(text="apple")
            return queryset

    spy = mocker.spy(TestVisibility, "visibility")

    VisibilitiesConfig.clear_handlers()
    VisibilitiesConfig.register_handler_class(TestVisibility)

    Model2.objects.create(text="none")
    model2 = Model2.objects.create(text="apple")

    model1 = Model1.objects.create(text="pear", model2=model2 if has_qs else None)

    if has_qs:
        model1.many.add(model2)
        model1.save()

    url = reverse("model1-detail", args=[model1.pk])
    response = admin_client.get(url)

    assert response.status_code == HTTP_200_OK
    result = response.json()

    if has_qs:
        assert spy.call_count == 3  # many, explicit (m2m) and model2 (fk)
    else:
        assert spy.call_count == 0

    assert result["text"] == "pear"

    if filter_relation or not has_qs:
        assert result["model2"] is None
        assert len(result["explicit"]) == 0
        assert len(result["many"]) == 0
    else:
        assert result["model2"] == model2.pk
        assert len(result["many"]) == 1
        assert len(result["explicit"]) == 1
        assert model2.pk in result["many"]
        assert model2.pk in result["explicit"]


def test_visibility_relation_patch(db, admin_user, admin_client):
    class TestVisibility:
        @filter_queryset_for(Model2)
        def filter_queryset_for_document(self, queryset, request):
            assert isinstance(request, Request)
            return queryset.exclude(text="apple")

    VisibilitiesConfig.clear_handlers()
    VisibilitiesConfig.register_handler_class(TestVisibility)

    model1 = Model1.objects.create(text="pear")
    Model2.objects.create(text="hidden")
    model2 = Model2.objects.create(text="apple")
    model3 = Model2.objects.create(text="melon")
    model4 = Model2.objects.create(text="orange")
    model1.many.add(model2)
    model1.many.add(model3)

    data = {"many": [model4.pk]}

    url = reverse("model1-detail", args=[model1.pk])
    response = admin_client.patch(url, data)

    assert response.status_code == HTTP_200_OK
    result = response.json()

    assert result["text"] == "pear"
    assert len(result["many"]) == 1
    assert model4.pk in result["many"]

    model1.refresh_from_db()
    assert model1.many.all().count() == 2
    assert model1.many.filter(pk=model2.pk).exists()
    assert model1.many.filter(pk=model4.pk).exists()


def test_visibility_related_field_check(db):
    class WrongSerializer(serializers.ModelSerializer):
        serializer_related_field = VisibilityPrimaryKeyRelatedField

        class Meta:
            model = Model1
            fields = "__all__"

    model1 = Model1.objects.create(text="pear")
    with pytest.raises(RuntimeWarning):
        serializer = WrongSerializer(model1)
        serializer.data  # noqa: B018


@pytest.mark.parametrize(
    "bypass_fields,expect_apple_many,expect_apple_one",
    [
        [{"tests.Model1": ["many"]}, True, False],
        [{"nonexistent.Model1": ["many"]}, False, False],
        [{"tests.Model1": []}, False, False],
        [{"tests.Model1": ["model2"]}, False, True],
        [{"tests.Model1": ["many", "model2"]}, True, True],
        [None, False, False],
        [{"tests.Model1": "__all__"}, True, True],
    ],
)
def test_visibility_bypass_field(
    db, admin_client, settings, bypass_fields, expect_apple_many, expect_apple_one
):
    class TestVisibility:
        @filter_queryset_for(Model2)
        def filter_queryset_for_model2(self, queryset, request):
            return queryset.exclude(text="apple")

    settings.GENERIC_PERMISSIONS_BYPASS_VISIBILITIES = bypass_fields
    VisibilitiesConfig.clear_handlers()
    VisibilitiesConfig.register_handler_class(TestVisibility)

    model1 = Model1.objects.create(text="pear")
    model2 = Model2.objects.create(text="apple")
    model3 = Model2.objects.create(text="melon")
    model1.model2 = model2
    model1.save()
    model1.many.add(model2)
    model1.many.add(model3)

    url = reverse("model1-detail", args=[model1.pk])
    response = admin_client.get(url)

    assert response.status_code == HTTP_200_OK
    result = response.json()

    assert (model2.pk in result["many"]) == expect_apple_many
    assert bool(result["model2"]) == expect_apple_one
