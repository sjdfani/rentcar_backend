from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser
from city.models import City


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Color(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=50)
    hex_code = models.CharField(verbose_name=_("HexCode"), max_length=50)
    status = models.BooleanField(verbose_name=_("Status"), default=True)

    def __str__(self) -> str:
        return self.name


class Category(BaseModel):
    name = models.CharField(verbose_name=_("Name"), max_length=50)
    status = models.BooleanField(verbose_name=_("Status"), default=True)

    def __str__(self) -> str:
        return self.name


class CarOptions(BaseModel):
    name = models.CharField(verbose_name=_("Name"), max_length=50)
    status = models.BooleanField(verbose_name=_("Status"), default=True)

    def __str__(self) -> str:
        return self.name


class Manufacturer(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"))

    def __str__(self) -> str:
        return self.name


class CarModel(BaseModel):
    manufacturers = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE,
        verbose_name=_("Manufacturer"),
    )
    name = models.CharField(max_length=255, verbose_name=_("Name"))

    def __str__(self) -> str:
        return self.name


class CarStyle(models.TextChoices):
    PASSENGER_CAR = ("passenger_car", "Passenger_Car")
    SUV = ("suv", "SUV")
    CONVERTIBLE = ("convertible", "Convertible")
    COUPE = ("coupe", "Coupe")
    VAN = ("van", "Van")
    PICKUP = ("pickup", "Pickup")


class GearboxType(models.TextChoices):
    MANUAL = ("manual", "Manual")
    AUTOMATIC = ("automatic", "Automatic")


class TechnicalSpecifications(BaseModel):
    body_style = models.CharField(
        verbose_name=_("Body Style"), max_length=15, choices=CarStyle.choices)
    gearbox_type = models.CharField(
        verbose_name=_("Gearbox Type"), max_length=9, choices=GearboxType.choices)
    cylinder = models.PositiveSmallIntegerField(
        verbose_name=_("Cylinder"), default=0)
    capacity = models.PositiveIntegerField(
        verbose_name=_("Capacity"), default=0)

    def __str__(self) -> str:
        return self.body_style


class CarTemplate(BaseModel):
    model = models.ForeignKey(
        CarModel, on_delete=models.CASCADE,
        verbose_name=_("Model"), related_name="CarTemplate_model"
    )
    Technical_specifications = models.ForeignKey(
        TechnicalSpecifications, on_delete=models.CASCADE,
        verbose_name=_("TechnicalSpecifications"), related_name="CarTemplate_TS"
    )
    category = models.ManyToManyField(Category, verbose_name=_("Category"))

    def __str__(self) -> str:
        return f"{self.model.manufacturers.name - self.model.name}"


class CarYear(BaseModel):
    name = models.CharField(verbose_name=_("Name"), max_length=50)
    status = models.BooleanField(verbose_name=_("Status"), default=True)

    def __str__(self) -> str:
        return self.name


class CarMileage(models.TextChoices):
    M0 = "0-50/000"
    M50 = "50/000-100/000"
    M100 = "100/000-200/000"
    M0200 = "+200/000"


class CarStatus(models.TextChoices):
    ACCEPTED = ("accepted", "Accepted")
    PENDING = ("pending", "Pending")
    REJECTED = ("rejected", "Rejected")


class Car(BaseModel):
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        verbose_name=_("Owner"), related_name="car_owner")
    car_template = models.ForeignKey(
        CarTemplate, on_delete=models.CASCADE,
        verbose_name=_("Car Template"), related_name="car_car_template")
    city = models.ForeignKey(
        City, on_delete=models.DO_NOTHING,
        verbose_name=_("City"), related_name="car_city")
    color = models.ForeignKey(
        Color, on_delete=models.DO_NOTHING,
        verbose_name=_("Car Color"), related_name="car_color")
    year = models.ForeignKey(
        CarYear, on_delete=models.DO_NOTHING,
        verbose_name=_("Car Year"), related_name="car_year")
    car_option = models.ManyToManyField(
        CarOptions, verbose_name=_("Car Options"))
    plate = models.CharField(
        verbose_name=_("Plate"), max_length=50, unique=True)
    description = models.TextField(
        verbose_name=_("Description"), null=True, blank=True)
    car_value = models.PositiveBigIntegerField(
        verbose_name=_("Car Value"), default=0)
    mileage = models.CharField(
        verbose_name=_("Mileage"), max_length=20, choices=CarMileage.choices)
    status = models.CharField(
        verbose_name=_("status"), max_length=10,
        choices=CarStatus.choices, default=CarStatus.PENDING)
    is_out_of_service = models.BooleanField(
        verbose_name=_("Is_out_of_Service"), default=False)
    has_media = models.BooleanField(verbose_name=_("Has_Media"), default=False)
    has_complete_info = models.BooleanField(
        verbose_name=_("Has_Complete_Info"), default=False)
    is_available = models.BooleanField(
        verbose_name=_("Is_Available"), default=False)

    def __str__(self) -> str:
        return self.owner.email

    def change_has_complete_info(self, value: bool):
        self.has_complete_info = value
        self.save()

    def change_has_media(self, value: bool):
        self.has_media = value
        self.save()


class CarImage(BaseModel):
    image = models.FileField(verbose_name=_("Image"), upload_to="images/")
    car_object = models.ForeignKey(
        Car, on_delete=models.CASCADE, verbose_name=_("Car"))

    def __str__(self) -> str:
        return self.car_object.owner


class Comment(BaseModel):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        verbose_name=_("User"), related_name="Comment_user")
    car_object = models.ForeignKey(
        Car, on_delete=models.CASCADE,
        verbose_name=_("Car"), related_name="Comment_car")
    text = models.TextField(verbose_name=_("text"))

    def __str__(self) -> str:
        return self.user.email


class RentalTerms(BaseModel):
    car_object = models.OneToOneField(
        Car, on_delete=models.CASCADE, verbose_name=_("Car"))
    cancellation_policy = models.TextField(
        verbose_name=_("Rental Cancellation Terms"))
    min_days_to_rent = models.PositiveIntegerField(
        verbose_name=_("Min Days to Rent"), default=0)
    max_km_per_day = models.PositiveIntegerField(
        verbose_name=_("Max KM Per Day"), default=0)
    extra_km_price = models.PositiveIntegerField(
        verbose_name=_("Extra KM Price"), default=0)
    extra_hour_price = models.PositiveIntegerField(
        verbose_name=_("Extra Hour Price"), default=0)
    deliver_at_renters_place = models.BooleanField(
        verbose_name=_("Deliver_at_Renters_Place"), default=False)
    with_driver = models.BooleanField(
        verbose_name=_("With_Driver"), default=False)
    without_driver = models.BooleanField(
        verbose_name=_("Without_Driver"), default=False)
    price_each_day = models.PositiveBigIntegerField(
        verbose_name=_("Price Each Day"), default=False)

    def __str__(self) -> str:
        return self.car_object.owner.email
