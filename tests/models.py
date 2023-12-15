from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """Base for test models that sets app_label, so they play nicely."""

    class Meta:
        app_label = "tests"
        abstract = True


class Model1(BaseModel):
    text = models.CharField(
        max_length=100,
        verbose_name=_("Text comes here"),
        help_text=_("Text description."),
    )
    model2 = models.ForeignKey(
        "tests.Model2",
        on_delete=models.CASCADE,
        related_name="model1s",
        verbose_name=_("Model2"),
        help_text=_("Model2 description."),
        null=True,
        blank=True,
    )
    many = models.ManyToManyField(
        "tests.Model2",
        related_name="model1s_many",
        verbose_name=_("Many"),
        help_text=_("Many description."),
        null=True,
        blank=True,
    )


class Model2(BaseModel):
    text = models.CharField(
        max_length=100,
        verbose_name=_("Text comes here"),
        help_text=_("Text description."),
    )
