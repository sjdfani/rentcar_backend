from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(_("Username"), max_length=20, unique=True)
    email = models.EmailField(_("Email address"), unique=True)
    photo = models.ImageField(
        upload_to="users/photo/", verbose_name=_("Photo"), null=True, blank=True)
    phone_number = models.CharField(
        _("Phone Number"), max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def update_last_login(self):
        self.last_login = timezone.now()
        self.save()


class EmailCode(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, verbose_name=_("User"))
    code = models.CharField(
        max_length=10, verbose_name=_("Code"), null=True, blank=True)
    unique_id = models.CharField(
        max_length=100, verbose_name=_("Unique ID"), null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False, verbose_name=_("Status"))

    def __str__(self) -> str:
        return self.user.email

    def set_unique_id_and_code(self, code):
        self.code = code
        self.unique_id = uuid.uuid4().hex
        self.status = True
        self.save()
