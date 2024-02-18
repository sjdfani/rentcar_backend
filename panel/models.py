from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser


class BasicPaymentInformation(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name=_("User"))
    company_percentage = models.FloatField(
        verbose_name=_("Company_Percentage"))
    value_added_percentage = models.FloatField(
        verbose_name=_("Value_Added_Percentage"))
    insurance_percentage = models.FloatField(
        verbose_name=_("Insurance_Percentage"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.email
