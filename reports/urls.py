from django.urls import path
from .views import (
    ReportByProduct, ReportByCategory, ReportByIsAvailable, ReportByBodyStyle,
    ReportByUserWithAcceptedCar, ReportByUser, ReportUsersAtLeastReserveCar,
)

app_name = "reports"

urlpatterns = [
    path("by/product/<str:type_>/", ReportByProduct.as_view(),
         name="ReportByProduct"),
    path("by/category/", ReportByCategory.as_view(),
         name="ReportByCategory"),
    path("by/is_available/", ReportByIsAvailable.as_view(),
         name="ReportByIsAvailable"),
    path("by/body_style/", ReportByBodyStyle.as_view(),
         name="ReportByBodyStyle"),

    path("by/users/car/accepted/", ReportByUserWithAcceptedCar.as_view(),
         name="ReportByUserWithAcceptedCar"),
    path("by/users/registered/", ReportByUser.as_view(),
         name="ReportUsersSerializer"),
    path("by/users/reserved/", ReportUsersAtLeastReserveCar.as_view(),
         name="ReportUsersAtLeastReserveCar"),
]
