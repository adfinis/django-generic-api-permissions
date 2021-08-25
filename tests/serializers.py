from rest_framework import serializers

from generic_permissions.validation import ValidatorMixin

from . import models


class TestModel1Serializer(ValidatorMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Model1
        fields = "__all__"


class TestModel2Serializer(ValidatorMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Model2
        fields = "__all__"
