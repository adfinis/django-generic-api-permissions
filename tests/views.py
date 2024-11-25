from rest_framework.permissions import BasePermission
from rest_framework.viewsets import ModelViewSet

from generic_permissions.permissions import PermissionViewMixin
from generic_permissions.visibilities import VisibilityViewMixin

from . import models, serializers


class BaseDenyAll(BasePermission):
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False


class Test1ViewSet(PermissionViewMixin, VisibilityViewMixin, ModelViewSet):
    serializer_class = serializers.TestModel1Serializer
    queryset = models.Model1.objects.all()


class Test2ViewSet(PermissionViewMixin, VisibilityViewMixin, ModelViewSet):
    serializer_class = serializers.TestModel2Serializer
    queryset = models.Model2.objects.all()


class TestBaseViewSet(PermissionViewMixin, VisibilityViewMixin, ModelViewSet):
    permission_classes = [BaseDenyAll]
    serializer_class = serializers.TestModel1Serializer
    queryset = models.Model1.objects.all()
