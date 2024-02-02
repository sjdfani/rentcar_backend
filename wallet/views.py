from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Wallet
from .serializers import (
    WalletSerializer,
)


class GetWalletByUser(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        wallet = Wallet.objects.get(user=self.request.user)
        wallet_data = WalletSerializer(wallet).data
        return Response(wallet_data, status=status.HTTP_200_OK)
