from rest_framework import serializers

from generic_permissions.validation import ValidatorMixin
from generic_permissions.visibilities import (
    VisibilityPrimaryKeyRelatedField,
    VisibilitySerializerMixin,
)

from . import models


class TestModel1Serializer(
    ValidatorMixin, VisibilitySerializerMixin, serializers.ModelSerializer
):
    serializer_related_field = VisibilityPrimaryKeyRelatedField
    explicit = VisibilityPrimaryKeyRelatedField(
        queryset=models.Model1.objects.all(), many=True, source="many"
    )

    class Meta:
        model = models.Model1
        fields = "__all__"


class TestModel2Serializer(ValidatorMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Model2
        fields = "__all__"
