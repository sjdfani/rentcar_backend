from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import (
    Manufacturer, CarModel, CarOptions, CarYear, Car, Color, CarStatus,
    Comment, RentalTerms,
)
from .serializers import (
    ManufacturerSerializer, CarModelSerializer, CarOptionsSerializer,
    CarYearSerializer, CreateCarSerializer, ColorSerializer, CarSerializer,
    CreateCommentSerializer, CreateRentalTermsSerializer,
    UpdateRentalTermsSerializer,
)

# Fix CarList -> date range
# change queryset of CarList


class ManufacturerList(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ManufacturerSerializer
    queryset = Manufacturer.objects.all()


class CarModelList(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CarModelSerializer

    def get_queryset(self):
        manufacturer = self.kwargs.get("manufacturer", None)
        if manufacturer:
            return CarModel.objects.filter(manufacturers__name=manufacturer)
        return CarModel.objects.none()


class CarOptionsList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CarOptionsSerializer
    queryset = CarOptions.objects.filter(status=True)


class CarYearList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CarYearSerializer
    queryset = CarYear.objects.filter(status=True)


class ColorList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ColorSerializer
    queryset = Color.objects.filter(status=True)


class CreateCar(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateCarSerializer
    queryset = Car.objects.all()


class CarList(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CarSerializer

    def get_queryset(self):
        return Car.objects.filter(
            status=CarStatus.ACCEPTED, is_out_of_service=False)


class RetrieveCar(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CarSerializer

    def get_queryset(self):
        return Car.objects.filter(
            status=CarStatus.ACCEPTED, is_out_of_service=False)


class RetrieveUpdateDestroyCar(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CarSerializer

    def get_queryset(self):
        return Car.objects.filter(owner=self.request.user)


class CreateComment(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateCommentSerializer
    queryset = Comment.objects.all()


class CreateRentalTerms(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateRentalTermsSerializer
    queryset = RentalTerms.objects.all()


class UpdateRentalTerms(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateRentalTermsSerializer

    def get_queryset(self):
        user = self.request.user
        pk = self.kwargs.get("pk", None)
        return RentalTerms.objects.filter(pk=pk, car_object__owner=user)
