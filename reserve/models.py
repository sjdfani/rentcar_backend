from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from users.models import CustomUser
from car.models import Car


class ReserveStatus(models.TextChoices):
    ACCEPTED = ("accepted", "Accepted")
    PENDING = ("pending", "Pending")
    REJECTED = ("rejected", "Rejected")


class Reserve(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        verbose_name=_("User"), related_name="reserve_user"
    )
    car = models.ForeignKey(
        Car, on_delete=models.DO_NOTHING,
        verbose_name=_("Car"), related_name="reserve_car"
    )
    start_rent_date = models.DateField(verbose_name=_("Start Rent Date"))
    min_days_to_rent = models.PositiveIntegerField(
        verbose_name=_("Min Days to Rent"), default=0)
    price_each_day = models.PositiveBigIntegerField(
        verbose_name=_("Price Each Day"), default=0)
    value_added = models.PositiveBigIntegerField(
        verbose_name=_("Value Added"), default=0)
    with_insurance = models.BooleanField(
        verbose_name=_("With_Insurance"), default=False)
    insurance_price = models.PositiveBigIntegerField(
        verbose_name=_("Insurance Price"), default=0)
    reserve_status = models.CharField(
        max_length=10, verbose_name=_("Reserver_Status"),
        choices=ReserveStatus.choices, default=ReserveStatus.PENDING
    )
    date_of_change_status = models.DateField(
        verbose_name=_("Date of Change Status"), null=True, blank=True)
    created_at = models.DateTimeField(
        verbose_name=_("Created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name=_("Updated_at"), auto_now=True)
    paid_date = models.DateTimeField(
        verbose_name=_("Paid Date"), null=True, blank=True)
    tracking_payment = models.CharField(
        max_length=20, verbose_name=_("Tracking Payment"), null=True, blank=True)
    bank_name = models.CharField(
        max_length=255, verbose_name=_("Bank Name"), null=True, blank=True)
    payment_status = models.BooleanField(
        verbose_name=_("Payment_Status"), default=False)

    def __str__(self) -> str:
        return self.user.email

    def payment_process(self, tracking_payment: str, bank_name: str):
        self.tracking_payment = tracking_payment
        self.bank_name = bank_name
        self.paid_date = timezone.now()
        self.payment_status = True
        self.car.is_available = False
        self.car.save()
        self.save()

    def change_status(self, status: ReserveStatus):
        self.reserve_status = status
        self.date_of_change_status = timezone.now()
        self.save()
