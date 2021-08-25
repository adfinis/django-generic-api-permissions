from warnings import warn

from .config import ValidatorsConfig

"""
Base for custom validations.

Extend this to implement your custom validators. The validation
methods will receive the data to be validated, and are expected to
return the data back to the caller.

You can modify the data, or raise a `ValidationError` if needed.

Additionally, you can access the request via `self.context['request'].`

Example:
>>> from generic_permissions.validation import BaseValidator, validator_for
>>> from my_project.my_app.models import User
>>> class LowercaseUsername:
...     @validator_for(User)
...     def lowercase_username(self, data):
...         data['username'] = data['username'].lower()
...         return data
"""

validator_for = ValidatorsConfig.decorator


class BaseValidator:
    def __init__(self, *args, **kwargs):  # pragma: no cover
        warn(
            DeprecationWarning(
                "BaseValidator is not required anymore. Just use "
                "a regular class without inheriting from BaseValidator"
            )
        )


class ValidatorMixin:
    def validate(self, *args, **kwargs):
        validated_data = super().validate(*args, **kwargs)

        for method in ValidatorsConfig.get_handlers(
            self.Meta.model,
        ):
            validated_data = method(validated_data, context=self.context)
        return validated_data
