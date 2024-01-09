from django.urls import path
from .views import (
    CreateManufacturer,
)

app_name = "car"

urlpatterns = [
    path("manufacturer/create/", CreateManufacturer.as_view(),
         name="CreateManufacturer"),
]
