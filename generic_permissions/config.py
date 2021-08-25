import inspect
from collections import defaultdict
from functools import wraps

from django.core.exceptions import ImproperlyConfigured


class MethodDecorator:
    def __init__(self, purpose_attr_name):
        self._attr_name = purpose_attr_name

    def __call__(self, model_cls):
        """Decorate custom validator method.

        Decorate your validator methods to mark which
        model they can be used for.
        """

        def _add_dgap_decoration(func):
            attr = getattr(func, self._attr_name, None)
            if attr:
                attr.append(model_cls)
                return func

            @wraps(func)
            def wrapped(*args, **kwargs):
                return func(*args, **kwargs)

            setattr(wrapped, self._attr_name, [model_cls])

            return wrapped

        return _add_dgap_decoration


class DGAPConfigManager:
    def __init__(self, purpose):
        self._purpose = purpose
        # Handlers map from model class -> list-of-handlers
        self._handlers = defaultdict(list)
        self._purpose_attr = f"_dgap_handler_for_{self._purpose}"

        self.decorator = MethodDecorator(self._purpose_attr)

    def get_handlers(self, model_cls, *args, **kwargs):
        """Return a list of callables to handle the given model.

        Additional args and kwargs can be passed - those will be used to
        initialize the handler class.
        """

        # There may be fallback handlers defined on a handler class.
        # We should only return the most specific handler for a given
        # model. The MRO list returns the "lowest", most-specific class
        # first, so we reverse the list, then use a dict to only keep
        # the last one (which will be the most-specific implementation
        # for the given model)

        all_available_lookup_classes = reversed(
            [
                lookup_cls
                for lookup_cls in model_cls.mro()
                if lookup_cls in self._handlers
            ]
        )

        handler_cls_and_method = {
            handler_cls: func_name
            for cls_to_handle in all_available_lookup_classes
            for handler_cls, func_name in self._handlers[cls_to_handle]
        }

        return [
            getattr(handler_cls(*args, **kwargs), func_name)
            for handler_cls, func_name in handler_cls_and_method.items()
        ]

    def register_handler_class(self, handler_cls):
        perm_fns = self.marked_methods(handler_cls)

        seen_models = set()
        for func_name, models in perm_fns:
            for model in models:
                if model in seen_models:
                    raise ImproperlyConfigured(
                        f"{handler_cls.__name__} has multiple methods "
                        f"registered for {self._purpose} on {model.__name__}. "
                        f"Last seen was {func_name}"
                    )
                seen_models.add(model)
                self._handlers[model].append((handler_cls, func_name))

    def _purpose_hasattr(self, handler):
        return hasattr(handler, self._purpose_attr)

    def _purpose_getattr(self, handler, default=None):
        return getattr(handler, self._purpose_attr, default)

    def marked_methods(self, handler_cls):
        return [
            (name, self._purpose_getattr(func))
            for name, func in inspect.getmembers(handler_cls, self._purpose_hasattr)
        ]

    def clear_handlers(self):
        """Clear model-specific handlers on this specific class.

        For instance, `ValidatorMixin.clear()` will clear all handlers of the
        `ValidatorMixin`, but not the ones of the `PermissionMixin` etc.
        """
        self._handlers = defaultdict(list)


PermissionsConfig = DGAPConfigManager(purpose="permission")
ObjectPermissionsConfig = DGAPConfigManager(purpose="object_permission")
VisibilitiesConfig = DGAPConfigManager(purpose="visibility")
ValidatorsConfig = DGAPConfigManager(purpose="validator")
