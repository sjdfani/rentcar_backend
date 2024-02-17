from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import (
    Manufacturer, CarModel, CarOptions, CarYear, Car, Color, CarStatus,
    Comment, RentalTerms,
)
from .serializers import (
    ManufacturerSerializer, CarModelSerializer, CarOptionsSerializer,
    CarYearSerializer, CreateCarSerializer, ColorSerializer, CarSerializer,
    CreateCommentSerializer, CreateRentalTermsSerializer,
    UpdateRentalTermsSerializer, UpdateCarSerializer,
)


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


class CreateCar(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CreateCarSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)


class CarListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CarList(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CarSerializer
    pagination_class = CarListPagination

    def get_queryset(self):
        city = self.request.query_params.get('city')

        if not city:
            return Car.objects.none()

        rental_terms_objects = RentalTerms.objects.all()

        rental_terms_filter = Q()
        if self.request.query_params.get('with_driver'):
            rental_terms_filter &= Q(with_driver=True)
        else:
            rental_terms_filter &= Q(with_driver=False)
        if self.request.query_params.get('without_driver'):
            rental_terms_filter &= Q(without_driver=True)
        else:
            rental_terms_filter &= Q(without_driver=False)
        if self.request.query_params.get('deliver_at_renters_place'):
            rental_terms_filter &= Q(deliver_at_renters_place=True)
        else:
            rental_terms_filter &= Q(deliver_at_renters_place=False)
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price is not None and max_price is not None:
            rental_terms_filter &= Q(price_each_day__gte=min_price) & Q(
                price_each_day__lte=max_price)

        rental_terms_objects = rental_terms_objects.filter(rental_terms_filter)
        car_ids = rental_terms_objects.values_list("car_object__id", flat=True)

        queryset = Car.objects.filter(
            id__in=car_ids,
            city__name=city,
            status=CarStatus.ACCEPTED,
            is_out_of_service=False,
            has_complete_info=True,
            is_available=True
        )

        if self.request.query_params.get('body_style'):
            queryset = queryset.filter(
                car_template__Technical_specifications__body_style=self.request.query_params.get('body_style'))
        if self.request.query_params.get('manufacturer'):
            queryset = queryset.filter(
                car_template__model__manufacturers__name=self.request.query_params.get('manufacturer'))
        if self.request.query_params.get('model'):
            queryset = queryset.filter(
                car_template__model__name=self.request.query_params.get('model'))

        return self.paginate_queryset(queryset)


class RetrieveCar(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CarSerializer

    def get_queryset(self):
        return Car.objects.filter(
            status=CarStatus.ACCEPTED, is_out_of_service=False, is_available=True)


class RetrieveUpdateDestroyCar(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CarSerializer
        return UpdateCarSerializer

    def get_queryset(self):
        return Car.objects.filter(owner=self.request.user)


class CarListByOwner(generics.ListAPIView):
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
