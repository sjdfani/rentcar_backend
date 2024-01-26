from rest_framework import generics
from users.permissions import IsSuperuser
from car.models import (
    Manufacturer, CarModel, Category, CarOptions, CarYear, CarTemplate, Car,
    Color, CarStatus, Comment,
)
from car.serializers import (
    ManufacturerSerializer, CarModelSerializer, CategorySerializer,
    CarOptionsSerializer, CarYearSerializer, CreateCarTemplateSerializer,
    CarTemplateSerializer, ColorSerializer, CarSerializer,  CommentSerializer,
    CreateCarModelSerializer,
)


class CreateManufacturer(generics.CreateAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = ManufacturerSerializer
    queryset = Manufacturer.objects.all()


class RetrieveUpdateDestroyManufacturer(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = ManufacturerSerializer
    queryset = Manufacturer.objects.all()


class CreateCarModel(generics.CreateAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CreateCarModelSerializer
    queryset = CarModel.objects.all()


class AllCarModelList(generics.ListAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CarModelSerializer
    queryset = CarModel.objects.all()


class RetrieveUpdateDestroyCarModel(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CarModelSerializer
    queryset = CarModel.objects.all()


class CreateCategory(generics.CreateAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryList(generics.ListAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class RetrieveUpdateDestroyCategory(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CreateCarOptions(generics.CreateAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CarOptionsSerializer
    queryset = CarOptions.objects.all()


class CarOptionsList(generics.ListAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CarOptionsSerializer
    queryset = CarOptions.objects.all()


class RetrieveUpdateDestroyCarOptions(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CarOptionsSerializer
    queryset = CarOptions.objects.all()


class CreateCarYear(generics.CreateAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CarYearSerializer
    queryset = CarYear.objects.all()


class CarYearList(generics.ListAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CarYearSerializer
    queryset = CarYear.objects.all()


class RetrieveUpdateDestroyCarYear(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CarYearSerializer
    queryset = CarYear.objects.all()


class CreateCarTemplate(generics.CreateAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CreateCarTemplateSerializer
    queryset = CarTemplate.objects.all()


class CarTemplateList(generics.ListAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CarTemplateSerializer
    queryset = CarTemplate.objects.all()


class RetrieveUpdateDestroyCarTemplate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CarTemplateSerializer
    queryset = CarTemplate.objects.all()


class CreateColor(generics.CreateAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = ColorSerializer
    queryset = Color.objects.all()


class ColorList(generics.ListAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = ColorSerializer
    queryset = Color.objects.all()


class RetrieveUpdateDestroyColor(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = ColorSerializer
    queryset = Color.objects.all()


class CommentList(generics.ListAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class RetrieveDestroyComment(generics.RetrieveDestroyAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class GetCarByStatus(generics.ListAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CarSerializer

    def get_queryset(self):
        status = self.kwargs.get("status", None)
        if status == CarStatus.ACCEPTED:
            return Car.objects.filter(status=CarStatus.ACCEPTED)
        elif status == CarStatus.PENDING:
            return Car.objects.filter(status=CarStatus.PENDING)
        elif status == CarStatus.REJECTED:
            return Car.objects.filter(status=CarStatus.REJECTED)
        return Car.objects.none()


class CarList(generics.ListAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CarSerializer
    queryset = Car.objects.all()
