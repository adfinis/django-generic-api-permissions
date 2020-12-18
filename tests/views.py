from rest_framework.viewsets import ModelViewSet

from generic_permissions.views import PermissionViewMixin, VisibilityViewMixin

from . import models, serializers


class TestViewSet(PermissionViewMixin, VisibilityViewMixin, ModelViewSet):
    serializer_class = serializers.TestModel1Serializer
    queryset = models.Model1.objects.all()
