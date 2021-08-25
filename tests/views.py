from rest_framework.viewsets import ModelViewSet

from generic_permissions.permissions import PermissionViewMixin
from generic_permissions.visibilities import VisibilityViewMixin

from . import models, serializers


class Test1ViewSet(PermissionViewMixin, VisibilityViewMixin, ModelViewSet):
    serializer_class = serializers.TestModel1Serializer
    queryset = models.Model1.objects.all()


class Test2ViewSet(PermissionViewMixin, VisibilityViewMixin, ModelViewSet):
    serializer_class = serializers.TestModel2Serializer
    queryset = models.Model2.objects.all()
