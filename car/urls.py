from django.urls import path
from .views import (
    ManufacturerList, CarModelList, CarOptionsList, CarYearList, RetrieveCar,
    CreateCar, CarList, RetrieveUpdateDestroyCar, ColorList, CreateComment,
    CreateRentalTerms,  UpdateRentalTerms, RetrieveRentalTerms, CarListByOwner,
)

app_name = "car"

urlpatterns = [
    path("manufacturer/list/", ManufacturerList.as_view(),
         name="ManufacturerList"),

    path("model/list/<str:manufacturer>/", CarModelList.as_view(),
         name="CarModelList"),

    path("options/list/", CarOptionsList.as_view(),
         name="CarOptionsList"),

    path("year/list/", CarYearList.as_view(),
         name="CarYearList"),

    path("color/list/", ColorList.as_view(),
         name="ColorList"),

    path("comment/create/", CreateComment.as_view(),
         name="CreateComment"),

    path("create/", CreateCar.as_view(),
         name="CreateCar"),
    path("list/", CarList.as_view(), name="car_list"),

    path("retrieve/<int:pk>/", RetrieveCar.as_view(),
         name="RetrieveCar"),
    path("list/<int:pk>/", RetrieveUpdateDestroyCar.as_view(),
         name="RetrieveUpdateDestroyCar"),
    path("list/owner/", CarListByOwner.as_view(), name="CarListByOwner"),

    path("rentalTerms/create/", CreateRentalTerms.as_view(),
         name="UpdateRentalTerms"),
    path("rentalTerms/retrieve/<int:pk>/", RetrieveRentalTerms.as_view(),
         name="RetrieveRentalTerms"),
    path("rentalTerms/update/<int:pk>/", UpdateRentalTerms.as_view(),
         name="UpdateRentalTerms"),
]
