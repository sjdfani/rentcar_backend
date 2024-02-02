from django.urls import path
from .views import (
    CreateManufacturer, ListReserveCar,  RetrieveUpdateDestroyManufacturer,
    CreateCarModel,  RetrieveUpdateDestroyCarModel, CreateCategory,
    RetrieveUpdateDestroyCategory, CategoryList, AllCarModelList,
    RetrieveUpdateDestroyCarOptions, CreateCarOptions, CreateCarYear,
    RetrieveUpdateDestroyCarYear, CreateCarTemplate, CarTemplateList,
    RetrieveUpdateDestroyCarTemplate, CreateColor, RetrieveUpdateDestroyColor,
    CommentList, RetrieveDestroyComment,  GetCarByStatus, CarOptionsList,
    CarYearList, ColorList, CarList, UpdateDestroyReserverCar, RetrieveUpdateDestroyCar,
    CreateBasicPaymentInformation, BasicPaymentInformationList,
    RetrieveUpdateDestroyBasicPaymentInformation,
)

app_name = "panel"

urlpatterns = [
    path("manufacturer/create/", CreateManufacturer.as_view(),
         name="CreateManufacturer"),
    path("manufacturer/list/<int:pk>/", RetrieveUpdateDestroyManufacturer.as_view(),
         name="RetrieveUpdateDestroyManufacturer"),

    path("car/model/create/", CreateCarModel.as_view(),
         name="CreateCarModel"),
    path("car/model/list/", AllCarModelList.as_view(),
         name="AllCarModelList"),
    path("car/model/list/<int:pk>/", RetrieveUpdateDestroyCarModel.as_view(),
         name="RetrieveUpdateDestroyCarModel"),

    path("category/create/", CreateCategory.as_view(),
         name="CreateCategory"),
    path("category/list/", CategoryList.as_view(),
         name="CategoryList"),
    path("category/list/<int:pk>/", RetrieveUpdateDestroyCategory.as_view(),
         name="RetrieveUpdateDestroyCategory"),

    path("car/options/create/", CreateCarOptions.as_view(),
         name="CreateCarOptions"),
    path("car/options/list/", CarOptionsList.as_view(),
         name="CarOptionsList"),
    path("car/options/list/<int:pk>/", RetrieveUpdateDestroyCarOptions.as_view(),
         name="RetrieveUpdateDestroyCarOptions"),

    path("year/create/", CreateCarYear.as_view(),
         name="CreateCarYear"),
    path("year/list/", CarYearList.as_view(),
         name="CarYearList"),
    path("year/list/<int:pk>/", RetrieveUpdateDestroyCarYear.as_view(),
         name="RetrieveUpdateDestroyCarYear"),

    path("template/create/", CreateCarTemplate.as_view(),
         name="CreateCarTemplate"),
    path("template/list/", CarTemplateList.as_view(),
         name="CarTemplateList"),
    path("template/list/<int:pk>/", RetrieveUpdateDestroyCarTemplate.as_view(),
         name="RetrieveUpdateDestroyCarTemplate"),

    path("color/create/", CreateColor.as_view(),
         name="CreateColor"),
    path("color/list/", ColorList.as_view(),
         name="ColorList"),
    path("color/list/<int:pk>/", RetrieveUpdateDestroyColor.as_view(),
         name="RetrieveUpdateDestroyColor"),

    path("comment/list/", CommentList.as_view(),
         name="CommentList"),
    path("comment/list/<int:pk>/", RetrieveDestroyComment.as_view(),
         name="RetrieveDestroyComment"),

    path("car/list/status/<str:status>/", GetCarByStatus.as_view(),
         name="GetCarByStatus"),
    path("car/all/list/", CarList.as_view(),
         name="CarList"),
    path("car/all/list/<int:pk>/", RetrieveUpdateDestroyCar.as_view(),
         name="RetrieveUpdateDestroyCar"),

    path("reserve/list/<str:status>/", ListReserveCar.as_view(),
         name="ListReserveCar"),
    path("reserve/all/list/<int:pk>/", UpdateDestroyReserverCar.as_view(),
         name="UpdateDestroyReserverCar"),

    path("basic-payment-info/create/", CreateBasicPaymentInformation.as_view(),
         name="CreateBasicPaymentInformation"),
    path("basic-payment-info/list/", BasicPaymentInformationList.as_view(),
         name="BasicPaymentInformationList"),
    path("basic-payment-info/list/<int:pk>/",
         RetrieveUpdateDestroyBasicPaymentInformation.as_view(),
         name="CreateBasicPaymentInformation"),
]
