from rest_framework import serializers
from reserve.models import Reserve
from django.utils import timezone
from .models import BasicPaymentInformation


class UpdateReserveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reserve
        exclude = (
            "user", "car", "updated_at", "date_of_change_status", "created_at")

    def update(self, instance, validated_data):
        result = super().update(instance, validated_data)
        if validated_data.get("reserve_status", None):
            instance.date_of_change_status = timezone.now()
            instance.save()
        return result


class BasicPaymentInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicPaymentInformation
        fields = "__all__"
