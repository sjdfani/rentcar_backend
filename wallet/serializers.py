from rest_framework import serializers
from .models import Wallet, withdrawal, Deposit
from django.utils import timezone


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"


class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"


class WithdrawalRequestSerializer(serializers.Serializer):
    description = serializers.CharField(required=False)

    def withdrawal_request(self):
        user = self.context["request"].user
        wallet = Wallet.objects.get(user=user)
        return withdrawal.objects.create(
            wallet=wallet,
            price=wallet.balance,
            description=self.validated_data.get("description", None),
            date_of_request=timezone.now(),
        )
