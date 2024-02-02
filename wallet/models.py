from django.db import models
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _
from reserve.models import Reserve


class Wallet(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, verbose_name=_("User"))
    balance = models.PositiveBigIntegerField(
        verbose_name=_("Balance"), default=0)
    card_number = models.CharField(
        max_length=20, verbose_name=_("Card Number"), null=True, blank=True)
    shaba_number = models.CharField(
        max_length=50, verbose_name=_("Shaba Number"), null=True, blank=True)
    account_number = models.CharField(
        max_length=40, verbose_name=_("Account Number"), null=True, blank=True)
    update_account_information_date = models.DateTimeField(
        verbose_name=_("Update Account Information Date"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.email

    def deposit_process(self, price: int):
        self.balance += price
        self.save()

    def withdrawal_process(self):
        self.balance = 0
        self.save()


class withdrawal(models.Model):
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, verbose_name=_("Wallet"))
    price = models.PositiveBigIntegerField(
        verbose_name=_("Price"), default=0)
    description = models.TextField(
        verbose_name=_("Description"), null=True, blank=True)
    paid_status = models.BooleanField(
        verbose_name=_("Paid_Status"), default=False)
    date_of_request = models.DateTimeField(
        verbose_name=_("Date_of_Request"))
    date_of_withdrawal = models.DateTimeField(
        verbose_name=_("Date_of_Withdrawal"), null=True, blank=True)
    tracking_payment = models.CharField(
        _("Tracking Payment"), max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.wallet.user.email


class Deposit(models.Model):
    reserve = models.ForeignKey(
        Reserve, on_delete=models.CASCADE, verbose_name=_("Reserve"))
    rent_price = models.PositiveBigIntegerField(verbose_name=_("Total_Price"))
    car_value = models.PositiveBigIntegerField(verbose_name=_("Car_Value"))
    company_percentage = models.PositiveIntegerField(
        verbose_name=_("Company_Percentage"))
    value_added_percentage = models.PositiveIntegerField(
        verbose_name=_("Value_Added_Percentage"))
    insurance_percentage = models.PositiveIntegerField(
        verbose_name=_("Insurance_Percentage"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.reserve.car.owner.email
