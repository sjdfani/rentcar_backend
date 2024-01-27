from django.urls import path
from .views import (
    CreateReserve, ListReserveCarOwner,
)

app_name = "reserve"

urlpatterns = [
    path("create/", CreateReserve.as_view(), name="CreateReserve"),
    path("list/owner/<str:status>/", ListReserveCarOwner.as_view(),
         name="ListReserveCarOwner"),
]
