from django.apps import AppConfig
from django.conf import settings
from django.utils.module_loading import import_string

from generic_permissions.config import (
    ObjectPermissionsConfig,
    PermissionsConfig,
    ValidatorsConfig,
    VisibilitiesConfig,
)
from generic_permissions.permissions import AllowAny
from generic_permissions.visibilities import Any


class GenericPermissionsConfig(AppConfig):
    name = "generic_permissions"
    verbose_name = "Django Generic API Permissions"

    def ready(self):
        self._init_config(
            "GENERIC_PERMISSIONS_PERMISSION_CLASSES",
            [AllowAny],
            [ObjectPermissionsConfig, PermissionsConfig],
        )

        self._init_config(
            "GENERIC_PERMISSIONS_VISIBILITY_CLASSES", [Any], [VisibilitiesConfig]
        )

        self._init_config(
            "GENERIC_PERMISSIONS_VALIDATOR_CLASSES", [], [ValidatorsConfig]
        )

    def _init_config(self, setting_name, defaults, configs):
        classes = defaults
        classes_strings = getattr(settings, setting_name, None)
        if classes_strings:
            classes = [import_string(name) for name in classes_strings]
        for c in configs:
            c.clear_handlers()
            for handler in classes:
                c.register_handler_class(handler)
