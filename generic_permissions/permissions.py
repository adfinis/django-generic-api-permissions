from warnings import warn

from django.core.exceptions import PermissionDenied

from .config import ObjectPermissionsConfig, PermissionsConfig

permission_for = PermissionsConfig.decorator
object_permission_for = ObjectPermissionsConfig.decorator


class PermissionViewMixin:
    def _check_permissions(self, request):
        """
        Check if access to model is granted.

        Raise PermissionDenied if configured permissions do not allow accesss to the model.
        """
        for handler in PermissionsConfig.get_handlers(self.get_serializer().Meta.model):
            if not handler(request):
                raise PermissionDenied()

    def check_permissions(self, request):
        """
        Overwrite default implementation to check DGAP permissions.
        """
        super().check_permissions(request)
        if request.method != "GET":
            self._check_permissions(request)

    def _check_object_permissions(self, request, instance):
        """
        Check if access to given object is granted.

        Raise PermissionDenied if configured permissions do not allow accesss to the object.
        """
        for handler in ObjectPermissionsConfig.get_handlers(
            self.get_serializer().Meta.model
        ):
            if not handler(request, instance):
                raise PermissionDenied()

    def check_object_permissions(self, request, instance):
        """
        Overwrite default implementation to check DGAP object permissions.
        """
        super().check_object_permissions(request, instance)
        if request.method != "GET":
            self._check_object_permissions(request, instance)


class BasePermission:
    def __init__(self, *args, **kwargs):  # pragma: no cover
        super().__init__(*args, **kwargs)
        warn(
            DeprecationWarning(
                "BasePermission is not required anymore. Just use "
                "a regular class without inheriting from BasePermission"
            ),
            stacklevel=2,
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
