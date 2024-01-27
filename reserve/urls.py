from django.urls import path
from .views import (
    CreateReserve, ListReserveCarOwner, ListReserveByCustomer, ChangeReserveStatus,
    PaymentReserve, FinishRentTime,
)

app_name = "reserve"

urlpatterns = [
    path("create/", CreateReserve.as_view(), name="CreateReserve"),
    path("list/owner/<str:status>/", ListReserveCarOwner.as_view(),
         name="ListReserveCarOwner"),
    path("list/customer/<str:status>/", ListReserveByCustomer.as_view(),
         name="ListReserveByCustomer"),
    path("status/", ChangeReserveStatus.as_view(), name="ChangeReserveStatus"),
    path("payment/", PaymentReserve.as_view(), name="PaymentReserve"),
    path("finish/", FinishRentTime.as_view(), name="FinishRentTime"),
]
