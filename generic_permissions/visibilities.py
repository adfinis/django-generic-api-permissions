from functools import reduce
from warnings import warn

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


class BaseVisibility:  # pragma: no cover
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        warn(
            DeprecationWarning(
                "BaseVisibility is not required anymore. Just use "
                "a regular class without inheriting from BaseVisibility"
            )
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
