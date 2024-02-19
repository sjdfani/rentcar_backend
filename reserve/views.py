from rest_framework.views import APIView
from rest_framework .response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import generics
from .models import Reserve, ReserveStatus
from .serializers import (
    CreateReserveSerializer, ReserveSerializer, ChangeReserveStatusSerializer,
    PaymentReserveSerializer, FinishRentTimeSerializer,
)


class CreateReserve(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = CreateReserveSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class ListReserveCarOwner(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ReserveSerializer

    def get_queryset(self):
        status_ = self.kwargs.get("status", None)
        if status_:
            if status_ == ReserveStatus.ACCEPTED:
                return Reserve.objects.filter(
                    car__owner=self.request.user, reserve_status=ReserveStatus.ACCEPTED)
            elif status_ == ReserveStatus.PENDING:
                return Reserve.objects.filter(
                    car__owner=self.request.user, reserve_status=ReserveStatus.PENDING)
            elif status_ == ReserveStatus.REJECTED:
                return Reserve.objects.filter(
                    car__owner=self.request.user, reserve_status=ReserveStatus.REJECTED)
        else:
            return Reserve.objects.none()


class ListReserveByCustomer(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ReserveSerializer

    def get_queryset(self):
        status_ = self.kwargs.get("status", None)
        if status_:
            if status_ == ReserveStatus.ACCEPTED:
                return Reserve.objects.filter(
                    user=self.request.user, reserve_status=ReserveStatus.ACCEPTED)
            elif status_ == ReserveStatus.PENDING:
                return Reserve.objects.filter(
                    user=self.request.user, reserve_status=ReserveStatus.PENDING)
            elif status_ == ReserveStatus.REJECTED:
                return Reserve.objects.filter(
                    user=self.request.user, reserve_status=ReserveStatus.REJECTED)
        else:
            return Reserve.objects.none()


class ChangeReserveStatus(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(Self, request):
        serializer = ChangeReserveStatusSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class PaymentReserve(APIView):
    def post(self, request):
        serializer = PaymentReserveSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class FinishRentTime(APIView):
    def post(self, request):
        serializer = FinishRentTimeSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
