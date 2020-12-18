from django.core.exceptions import ImproperlyConfigured, PermissionDenied


class VisibilityModelMixin:
    visibility_classes = None

    @classmethod
    def visibility_queryset_filter(cls, queryset, request, **kwargs):
        if cls.visibility_classes is None:
            raise ImproperlyConfigured(
                "check that app `dpv` is part of your `INSTALLED_APPS`."
            )

        for visibility_class in cls.visibility_classes:
            queryset = visibility_class().filter_queryset(cls, queryset, request)

        return queryset


class PermissionModelMixin:
    permission_classes = None

    @classmethod
    def check_permissions(cls, request, **kwargs):
        if cls.permission_classes is None:
            raise ImproperlyConfigured(
                "check that app `dpv` is part of your `INSTALLED_APPS`."
            )

        for permission_class in cls.permission_classes:
            if not permission_class().has_permission(cls, request):
                raise PermissionDenied()

    def check_object_permissions(self, request):
        for permission_class in self.permission_classes:
            if not permission_class().has_object_permission(
                self.__class__, request, self
            ):
                raise PermissionDenied()
