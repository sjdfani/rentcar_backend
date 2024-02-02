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
        withdrawal.objects.create(
            wallet=wallet,
            price=wallet.balance,
            description=self.validated_data.get("description", None),
            date_of_request=timezone.now(),
        )
        wallet.withdrawal_process()


class DoneWithdrawalSerializer(serializers.Serializer):
    withdrawal_obj = serializers.PrimaryKeyRelatedField(
        queryset=withdrawal.objects.all()
    )
    tracking_payment = serializers.CharField()

    def done_withdrawal_process(self):
        obj = self.validated_data["withdrawal_obj"]
        obj.paid_status = True
        obj.tracking_payment = self.validated_data["tracking_payment"]
        obj.date_of_withdrawal = timezone.now()
        obj.save()
