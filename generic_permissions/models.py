from warnings import warn


class VisibilityModelMixin:
    def __init__(self, *args, **kwargs):  # pragma: no cover
        super().__init__(*args, **kwargs)
        warn(
            DeprecationWarning(
                "VisibilityModelMixin is not required anymore and "
                "will be removed in a future version of DGAP"
            )
        )


class PermissionModelMixin:
    def __init__(self, *args, **kwargs):  # pragma: no cover
        super().__init__(*args, **kwargs)
        warn(
            DeprecationWarning(
                "PermissionModelMixin is not required anymore and "
                "will be removed in a future version of DGAP"
            )
        )
