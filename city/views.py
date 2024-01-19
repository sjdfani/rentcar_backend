from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import CitySerializer
from .models import City
from users.permissions import IsSuperuser


class CreateCity(generics.CreateAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CitySerializer
    queryset = City.objects.all()


class CityList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CitySerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return City.objects.all()
        return City.objects.filter(status=True)


class RetrieveUpdateDestroyCity(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CitySerializer
    queryset = City.objects.all()
