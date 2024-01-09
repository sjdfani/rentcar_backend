from rest_framework import generics
from .models import Manufacturer
from users.permissions import IsSuperuser
from .serializers import (
    ManufacturerSerializer,
)


class CreateManufacturer(generics.CreateAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = ManufacturerSerializer
    queryset = Manufacturer.objects.all()


class ManufacturerList(generics.ListAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = ManufacturerSerializer
    queryset = Manufacturer.objects.all()


class RetrieveUpdateDestroyManufacturer(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = ManufacturerSerializer
    queryset = Manufacturer.objects.all()
