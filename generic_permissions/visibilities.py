from functools import reduce
from warnings import warn

from django.conf import settings
from rest_framework.relations import MANY_RELATION_KWARGS, ManyRelatedField
from rest_framework.serializers import PrimaryKeyRelatedField

from .config import DGAPConfigManager, VisibilitiesConfig

"""
Basic visibility classes to be extended by any visibility implementation.

In combination with the decorator `@filter_queryset_for` a custom
visibility class can define filtering on basis of models.

A custom visibility class could look like this:
```
>>> from generic_permissions.visibilities import BaseVisibility
... from tests.models import BaseModel, Model1, Model2
...
...
... class CustomVisibility:
...     @filter_queryset_for(BaseModel)
...     def filter_queryset_for_all(self, queryset, request):
...         return queryset.filter(created_by_user=request.user.username)
...
...     @filter_queryset_for(Model1)
...     def filter_queryset_for_document(self, queryset, request):
...         return queryset.exclude(category__slug='protected-category')
...
...     @filter_queryset_for(Model2)
...     def filter_queryset_for_file(self, queryset, request):
...         # Limitations for `Model1` should also be enforced on `Model2`.
...         return queryset.exclude(document__category__slug='protected-category')
```
"""


filter_queryset_for = VisibilitiesConfig.decorator


def _should_bypass_field(instance, field_name: str) -> bool:
    bypass_fields_settings = (
        getattr(settings, "GENERIC_PERMISSIONS_BYPASS_VISIBILITIES", {}) or {}
    )

    meta = getattr(instance, "_meta", None) or getattr(instance, "Meta", None)
    app_label = getattr(meta, "app_label", "")
    bypass_fields = bypass_fields_settings.get(
        f"{app_label}.{type(instance).__name__}",
        [],
    )

    if bypass_fields == "__all__":
        return True

    return field_name in bypass_fields


class VisibilityViewMixin:
    def get_queryset(self):
        queryset = super().get_queryset()

        if not queryset.exists():
            return queryset

        for handler in VisibilitiesConfig.get_handlers(queryset.model):
            queryset = handler(queryset, self.request)

        return queryset


class VisibilityManyRelatedField(ManyRelatedField):
    def get_attribute(self, instance):
        queryset = super().get_attribute(instance)

        if not queryset.exists():
            return queryset

        if _should_bypass_field(instance, self.field_name):
            return queryset

        for handler in VisibilitiesConfig.get_handlers(queryset.model):
            queryset = handler(queryset, self.parent._context["request"])

        return queryset


class VisibilitySerializerMixin:
    """
    Mixin for serializers to handle visibility of related fields.

    This mixin ensures that when updating (PATCH) existing relationships,
    any relationships not included in the request (due to visibility settings)
    are not unintentionally removed. It does this by adding back the existing relations
    which are not included in the request.

    This mixin should be used in conjunction with the `VisibilityRelatedFieldMixin`
    for the relationship field and should be defined after the `ValidatorMixin`
    to ensure validations are performed first.
    """

    def validate(self, *args, **kwargs):
        validated_data = super().validate(*args, **kwargs)

        if not self.instance:
            return validated_data

        # Incoming patches can have a subset of all relations, so we need to
        # keep the existing relations which are not included in the request.
        for key, field in self.fields.items():
            if (
                not isinstance(field, VisibilityManyRelatedField)
                or key not in validated_data
            ):
                continue

            # Find the relations which the request can include.
            queryset = getattr(self.instance, key).all()
            for handler in VisibilitiesConfig.get_handlers(queryset.model):
                queryset = handler(queryset, self.context["request"])

            # Add remaining relations which can not be included in the request.
            validated_data[key] += getattr(self.instance, key).exclude(pk__in=queryset)

        return validated_data


class VisibilityRelatedFieldMixin:
    @classmethod
    def many_init(cls, *args, **kwargs):
        # ManyToManyField
        list_kwargs = {"child_relation": cls(*args, **kwargs)}
        for key in kwargs:
            if key in MANY_RELATION_KWARGS:
                list_kwargs[key] = kwargs[key]

        return VisibilityManyRelatedField(**list_kwargs)

    def get_attribute(self, instance):
        # ForeignKey
        model_instance = super().get_attribute(instance)

        if _should_bypass_field(instance, self.field_name):
            return model_instance

        if model_instance.pk is None:
            return None

        # read only fields don't have queryset, infer it from the model
        queryset = self.queryset or type(instance).objects
        queryset = queryset.filter(pk=model_instance.pk)

        for handler in VisibilitiesConfig.get_handlers(queryset.model):
            queryset = handler(queryset, self.parent._context["request"])

        if not queryset.filter(pk=model_instance.pk).exists():
            return None

        return model_instance

    def bind(self, field_name, parent):
        if isinstance(parent, VisibilityManyRelatedField):
            return super().bind(field_name, parent)

        if not isinstance(parent, VisibilitySerializerMixin):
            raise RuntimeWarning(
                f"To avoid data loss, use VisibilitySerializerMixin in {type(parent).__name__}"
            )
        return super().bind(field_name, parent)


class VisibilityPrimaryKeyRelatedField(
    VisibilityRelatedFieldMixin, PrimaryKeyRelatedField
):
    """Visibility-aware replacement for DRF PrimaryKeyRelatedField."""

    pass


try:
    from rest_framework_json_api.relations import (
        ResourceRelatedField,
        SerializerMethodResourceRelatedField,
    )

    class VisibilityResourceRelatedField(
        VisibilityRelatedFieldMixin, ResourceRelatedField
    ):
        """Visibility-aware replacement for DRF-JSONAPI ResourceRelatedField."""

        pass

    class VisibilitySerializerMethodResourceRelatedField(
        VisibilityRelatedFieldMixin, SerializerMethodResourceRelatedField
    ):
        """Visibility-aware replacement for DRF-JSONAPI SerializerMethodResourceRelatedField."""

        pass

except ModuleNotFoundError:  # pragma: no cover
    if settings.DEBUG:
        print(
            "django-rest-framework-json-api is not installed. Skipping django-rest-framework-json-api related imports."
        )


class BaseVisibility:  # pragma: no cover
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        warn(
            DeprecationWarning(
                "BaseVisibility is not required anymore. Just use "
                "a regular class without inheriting from BaseVisibility"
            ),
            stacklevel=2,
        )


class Any:
    """No restrictions, all models are exposed."""

    pass


class Union:
    """Union result of a list of configured visibility classes."""

    visibility_classes = []

    def __init__(self):
        self._config = DGAPConfigManager("visibility")
        for cls in self.visibility_classes:
            self._config.register_handler_class(cls)

    @filter_queryset_for(object)
    def filter_queryset(self, queryset, request):
        handlers = self._config.get_handlers(queryset.model)
        querysets_to_merge = [handler(queryset, request) for handler in handlers]

        union_qs = reduce(lambda a, b: a.union(b), querysets_to_merge, queryset.none())

        return queryset.filter(pk__in=union_qs.values("pk"))
