from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from car.models import Car, CarStatus
from django.db.models import Count
from .serializers import (
    ReportUsersWithAcceptedCarSerializer, ReportUsersSerializer,
    ReportUsersAtLeastReserveCarSerializer,
)


class ReportByProduct(APIView):
    def get(self, request, type_):
        if type_ == "accepted_cars":
            accepted_cars_count = Car.objects.filter(
                status=CarStatus.ACCEPTED).count()
            all_cars_count = Car.objects.all().count()
            message = {
                "accepted_cars_count": accepted_cars_count,
                "all_cars_count": all_cars_count,
            }
        elif type_ == "manufacturer":
            manufacturer_counts = Car.objects.values('car_template__model__manufacturers__name').annotate(
                count=Count('car_template__model__manufacturers__name'))
            message = {
                item['car_template__model__manufacturers__name']: item['count'] for item in manufacturer_counts}
        elif type_ == "car_year":
            car_year_counts = Car.objects.values(
                'year__name').annotate(count=Count('year__name'))
            message = {
                item['year__name']: item['count'] for item in car_year_counts}
        return Response(message, status=status.HTTP_200_OK)


class ReportByCategory(APIView):
    def get(self, request):
        car_category_counts = Car.objects.values('car_template__category__name').annotate(
            count=Count('car_template__category__name'))
        message = {
            item['car_template__category__name']: item['count'] for item in car_category_counts}
        return Response(message, status=status.HTTP_200_OK)


class ReportByIsAvailable(APIView):
    def get(self, request):
        car_is_available_counts = Car.objects.filter(is_available=True).count()
        message = {
            "car_is_available_counts": car_is_available_counts,
        }
        return Response(message, status=status.HTTP_200_OK)


class ReportByBodyStyle(APIView):
    def get(self, request):
        car_style_counts = Car.objects.values('car_template__Technical_specifications__body_style').annotate(
            count=Count('car_template__Technical_specifications__body_style'))
        message = {
            item['car_template__Technical_specifications__body_style']: item['count'] for item in car_style_counts}
        return Response(message, status=status.HTTP_200_OK)


class ReportByUserWithAcceptedCar(APIView):
    def post(self, request):
        serializer = ReportUsersWithAcceptedCarSerializer(
            data=request.data, context={"request", request}
        )
        serializer.is_valid(raise_exception=True)
        message = serializer.get_data()
        return Response(message, status=status.HTTP_200_OK)


class ReportByUser(APIView):
    def post(self, request):
        serializer = ReportUsersSerializer(
            data=request.data, context={"request", request}
        )
        serializer.is_valid(raise_exception=True)
        message = serializer.get_data()
        return Response(message, status=status.HTTP_200_OK)


class ReportUsersAtLeastReserveCar(APIView):
    def post(self, request):
        serializer = ReportUsersAtLeastReserveCarSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        message = serializer.get_data()
        return Response(message, status=status.HTTP_200_OK)
