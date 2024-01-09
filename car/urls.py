from django.urls import path
from .views import (
    CreateManufacturer, ManufacturerList, RetrieveUpdateDestroyManufacturer,
)

app_name = "car"

urlpatterns = [
    path("manufacturer/create/", CreateManufacturer.as_view(),
         name="CreateManufacturer"),
    path("manufacturer/list/", ManufacturerList.as_view(),
         name="ManufacturerList"),
    path("manufacturer/list/<int:pk>/", RetrieveUpdateDestroyManufacturer.as_view(),
         name="ManufacturerList"),
]
