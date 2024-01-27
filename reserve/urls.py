from django.urls import path
from .views import (
    CreateReserve,
)

app_name = "reserve"

urlpatterns = [
    path("create/", CreateReserve.as_view(), name="CreateReserve"),
]
