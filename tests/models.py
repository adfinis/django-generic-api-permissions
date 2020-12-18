from django.db import models
from django.utils.translation import gettext_lazy as _

from generic_permissions.models import PermissionModelMixin, VisibilityModelMixin


class BaseModel(models.Model):
    """
    Base for test models that sets app_label, so they play nicely.
    """

    class Meta:
        app_label = "tests"
        abstract = True


class Model1(PermissionModelMixin, VisibilityModelMixin, BaseModel):
    text = models.CharField(
        max_length=100,
        verbose_name=_("Text comes here"),
        help_text=_("Text description."),
    )


class Model2(PermissionModelMixin, VisibilityModelMixin, BaseModel):
    text = models.CharField(
        max_length=100,
        verbose_name=_("Text comes here"),
        help_text=_("Text description."),
    )
