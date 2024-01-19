from django.db import models
from django.utils.translation import gettext_lazy as _


class City(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=50)
    status = models.BooleanField(verbose_name=_("Status"), default=True)

    def __str__(self) -> str:
        return self.name
