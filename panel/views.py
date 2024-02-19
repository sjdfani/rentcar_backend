from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from reserve.models import Reserve, ReserveStatus
from reserve.serializers import ReserveSerializer
from users.permissions import IsSuperuser
from car.models import (
    Manufacturer, CarModel, Category, CarOptions, CarYear, CarTemplate, Car,
    Color, CarStatus, Comment,
)
from car.serializers import (
    ManufacturerSerializer, CarModelSerializer, CategorySerializer,
    CarOptionsSerializer, CarYearSerializer, CreateCarTemplateSerializer,
    CarTemplateSerializer, ColorSerializer, CarSerializer,  CommentSerializer,
    CreateCarModelSerializer, UpdateCarTemplateSerializer,
)
from .serializers import UpdateReserveSerializer, BasicPaymentInformationSerializer
from .models import BasicPaymentInformation
from wallet.models import withdrawal, Deposit, Wallet
from wallet.serializers import WithdrawalSerializer, DepositSerializer, WalletSerializer


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


class CreateCarTemplate(APIView):
    permission_classes = (IsSuperuser,)

    def post(self, request):
        serializer = CreateCarTemplateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class CarTemplateList(generics.ListAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CarTemplateSerializer
    queryset = CarTemplate.objects.all()


class RetrieveUpdateDestroyCarTemplate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperuser,)
    queryset = CarTemplate.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["GET", "DELETE"]:
            return CarTemplateSerializer
        return UpdateCarTemplateSerializer


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


class RetrieveUpdateDestroyCar(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = CarSerializer
    queryset = Car.objects.all()


class ListReserveCar(generics.ListAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = ReserveSerializer

    def get_queryset(self):
        status_ = self.kwargs.get("status", None)
        if status_:
            if status_ == ReserveStatus.ACCEPTED:
                return Reserve.objects.filter(reserve_status=ReserveStatus.ACCEPTED)
            elif status_ == ReserveStatus.PENDING:
                return Reserve.objects.filter(reserve_status=ReserveStatus.PENDING)
            elif status_ == ReserveStatus.REJECTED:
                return Reserve.objects.filter(reserve_status=ReserveStatus.REJECTED)
        else:
            return Reserve.objects.none()


class UpdateDestroyReserverCar(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperuser,)
    queryset = Reserve.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReserveSerializer
        return UpdateReserveSerializer


class CreateBasicPaymentInformation(generics.CreateAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = BasicPaymentInformationSerializer
    queryset = BasicPaymentInformation.objects.all()


class BasicPaymentInformationList(generics.ListAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = BasicPaymentInformationSerializer
    queryset = BasicPaymentInformation.objects.all()


class RetrieveUpdateDestroyBasicPaymentInformation(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = BasicPaymentInformationSerializer
    queryset = BasicPaymentInformation.objects.all()


class WithdrawalList(generics.ListAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = WithdrawalSerializer
    queryset = withdrawal.objects.all()


class DepositList(generics.ListAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = DepositSerializer
    queryset = Deposit.objects.all()


class WalletList(generics.ListAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
