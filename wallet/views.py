from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Wallet, withdrawal, Deposit
from .serializers import (
    WalletSerializer, WithdrawalRequestSerializer, WithdrawalSerializer,
    DoneWithdrawalSerializer, DepositSerializer,
)


class GetWalletByUser(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        wallet = Wallet.objects.get(user=self.request.user)
        wallet_data = WalletSerializer(wallet).data
        return Response(wallet_data, status=status.HTTP_200_OK)


class WithdrawalRequest(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = WithdrawalRequestSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        data = WithdrawalSerializer(
            serializer.withdrawal_request()).data
        return Response(data, status=status.HTTP_201_CREATED)


class DoneWithdrawal(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = DoneWithdrawalSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WithdrawalList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WithdrawalSerializer

    def get_queryset(self):
        return withdrawal.objects.filter(wallet__user=self.request.user)


class DepositListByOwner(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DepositSerializer

    def get_queryset(self):
        return Deposit.objects.filter(reserve__owner=self.request.user)


class DepositListByUser(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DepositSerializer

    def get_queryset(self):
        return Deposit.objects.filter(reserve__user=self.request.user)
