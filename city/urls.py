from django.urls import path
from .views import CreateCity, CityList, RetrieveUpdateDestroyCity

app_name = "city"

urlpatterns = [
    path("create/", CreateCity.as_view(), name="CreateCity"),
    path("list/", CityList.as_view(), name="CityList"),
    path("list/<int:pk>/", RetrieveUpdateDestroyCity.as_view(),
         name="RetrieveUpdateDestroyCity"),
]
