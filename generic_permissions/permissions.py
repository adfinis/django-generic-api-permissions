from warnings import warn

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from .config import ObjectPermissionsConfig, PermissionsConfig

permission_for = PermissionsConfig.decorator
object_permission_for = ObjectPermissionsConfig.decorator


class PermissionViewMixin:
    def destroy(self, request, *args, **kwargs):
        self._check_permissions(request)
        instance = self.get_object()

        # we do not call `super()` in order to not fetch the object twice.
        self.perform_destroy(instance)
        return HttpResponse(status=204)

    def create(self, request, *args, **kwargs):
        self._check_permissions(request)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self._check_permissions(request)
        return super().update(request, *args, **kwargs)

    def _check_permissions(self, request):
        for handler in PermissionsConfig.get_handlers(self.get_serializer().Meta.model):
            if not handler(request):
                raise PermissionDenied()

    def check_object_permissions(self, request, instance):
        """Check if access to given object is granted.

        Raise PermissionDenied if configured permissions do not allow
        accesss to the object.

        Called by get_object().
        """
        for handler in ObjectPermissionsConfig.get_handlers(
            self.get_serializer().Meta.model
        ):
            if not handler(request, instance):
                raise PermissionDenied()


class BasePermission:
    def __init__(self, *args, **kwargs):  # pragma: no cover
        super().__init__(*args, **kwargs)
        warn(
            DeprecationWarning(
                "BasePermission is not required anymore. Just use "
                "a regular class without inheriting from BasePermission"
            )
        )


class AllowAny:
    @permission_for(object)
    def default_permission(self, request):
        return True

    @object_permission_for(object)
    def default_object_permission(self, request, instance):
        return True


class DenyAll:
    @permission_for(object)
    def default_permission(self, request):
        return False

    @object_permission_for(object)
    def default_object_permission(self, request, instance):
        return False
