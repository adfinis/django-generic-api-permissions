from warnings import warn  # pragma: no cover

from generic_permissions import permissions, visibilities  # pragma: no cover


class VisibilityViewMixin(visibilities.VisibilityViewMixin):  # pragma: no cover
    def __init__(self, *args, **kwargs):
        warn(
            DeprecationWarning(
                "VisibilityViewMixin has moved from generic_permissions.views "
                "to generic_permissions.visibilities. Please update your imports"
            )
        )
        super().__init__(*args, **kwargs)


class PermissionViewMixin(permissions.PermissionViewMixin):  # pragma: no cover
    def __init__(self, *args, **kwargs):
        warn(
            DeprecationWarning(
                "PermissionViewMixin has moved from generic_permissions.views "
                "to generic_permissions.permissions. Please update your imports"
            )
        )
        super().__init__(*args, **kwargs)
