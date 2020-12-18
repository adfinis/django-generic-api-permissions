class PermissionSerializerMixin:
    def validate(self, *args, **kwargs):
        validated_data = super().validate(*args, **kwargs)

        self.Meta.model.check_permissions(self.context["request"])
        if self.instance is not None:
            self.instance.check_object_permissions(self.context["request"])

        return validated_data
