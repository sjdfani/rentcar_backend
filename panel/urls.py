from django.urls import path
from .views import (
    CreateManufacturer,  RetrieveUpdateDestroyManufacturer,
    CreateCarModel,  RetrieveUpdateDestroyCarModel, CreateCategory,
    RetrieveUpdateDestroyCategory, CategoryList, AllCarModelList,
    RetrieveUpdateDestroyCarOptions, CreateCarOptions, CreateCarYear,
    RetrieveUpdateDestroyCarYear, CreateCarTemplate, CarTemplateList,
    RetrieveUpdateDestroyCarTemplate, CreateColor, RetrieveUpdateDestroyColor,
    CommentList, RetrieveDestroyComment,  GetCarByStatus,
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
    path("car/options/list/<int:pk>/", RetrieveUpdateDestroyCarOptions.as_view(),
         name="RetrieveUpdateDestroyCarOptions"),

    path("year/create/", CreateCarYear.as_view(),
         name="CreateCarYear"),
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
    path("color/list/<int:pk>/", RetrieveUpdateDestroyColor.as_view(),
         name="RetrieveUpdateDestroyColor"),

    path("comment/list/", CommentList.as_view(),
         name="CommentList"),
    path("comment/list/<int:pk>/", RetrieveDestroyComment.as_view(),
         name="RetrieveDestroyComment"),

    path("car/list/status/<str:status>/", GetCarByStatus.as_view(),
         name="GetCarByStatus"),
]
