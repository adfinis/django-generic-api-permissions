from warnings import warn  # pragma: no cover


class PermissionSerializerMixin:  # pragma: no cover
    def __init__(self, *args, **kwargs):
        warn(
            DeprecationWarning(
                "PermissionSerializerMixin is not required anymore. You "
                "only need to decorate your viewsets now, using "
                "generic_permissions.permissions.PermissionViewMixin."
            )
        )
        super().__init__(*args, **kwargs)
