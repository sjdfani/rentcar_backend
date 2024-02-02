from rest_framework import serializers
from .models import Wallet, withdrawal, Deposit


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"
