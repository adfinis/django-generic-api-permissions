from functools import reduce
from warnings import warn

from rest_framework.relations import MANY_RELATION_KWARGS, ManyRelatedField
from rest_framework.serializers import PrimaryKeyRelatedField
from rest_framework_json_api.relations import (
    ResourceRelatedField,
    SerializerMethodResourceRelatedField,
)

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


class VisibilityViewMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        for handler in VisibilitiesConfig.get_handlers(queryset.model):
            queryset = handler(queryset, self.request)

        return queryset


class VisibilityManyRelatedField(ManyRelatedField):
    def get_attribute(self, instance):
        queryset = super().get_attribute(instance)
        for handler in VisibilitiesConfig.get_handlers(queryset.model):
            queryset = handler(queryset, self.parent._context["request"])

        return queryset


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

        if model_instance.pk is None:
            return None

        # create a queryset with the current model instance to check visibility
        queryset = self.queryset.filter(pk=model_instance.pk)
        for handler in VisibilitiesConfig.get_handlers(queryset.model):
            queryset = handler(queryset, self.parent._context["request"])

        if not queryset.filter(pk=model_instance.pk).exists():
            return None

        return model_instance


class VisibilityPrimaryKeyRelatedField(
    VisibilityRelatedFieldMixin, PrimaryKeyRelatedField
):
    """Visibility-aware replacement for DRF PrimaryKeyRelatedField."""

    pass


class VisibilityResourceRelatedField(VisibilityRelatedFieldMixin, ResourceRelatedField):
    """Visibility-aware replacement for DRF-JSONAPI ResourceRelatedField."""

    pass


class VisibilitySerializerMethodResourceRelatedField(
    VisibilityRelatedFieldMixin, SerializerMethodResourceRelatedField
):
    """Visibility-aware replacement for DRF-JSONAPI SerializerMethodResourceRelatedField."""

    pass


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
