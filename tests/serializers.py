from rest_framework import serializers

from generic_permissions.serializers import PermissionSerializerMixin

from . import models


class TestModel1Serializer(PermissionSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Model1
        fields = "__all__"
