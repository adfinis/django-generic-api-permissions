from django.apps import AppConfig
from django.conf import settings
from django.utils.module_loading import import_string

from generic_permissions.permissions import AllowAny
from generic_permissions.visibilities import Any


class GenericPermissionsConfig(AppConfig):
    name = "generic_permissions"
    verbose_name = "Django Generic API Permissions"

    def ready(self):
        # to avoid recursive import error, load extension classes
        # only once the app is ready
        from .models import PermissionModelMixin, VisibilityModelMixin

        permission_classes = [AllowAny]
        permission_classes_strings = getattr(
            settings, "GENERIC_PERMISSIONS_PERMISSION_CLASSES", None
        )
        if permission_classes_strings:
            permission_classes = [
                import_string(cls) for cls in permission_classes_strings
            ]
        PermissionModelMixin.permission_classes = permission_classes

        visibility_classes = [Any]
        visibility_classes_strings = getattr(
            settings, "GENERIC_PERMISSIONS_VISIBILITY_CLASSES", None
        )
        if visibility_classes_strings:
            visibility_classes = [
                import_string(cls)
                for cls in settings.GENERIC_PERMISSIONS_VISIBILITY_CLASSES
            ]
        VisibilityModelMixin.visibility_classes = visibility_classes
