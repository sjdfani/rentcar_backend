from rest_framework import serializers
from reserve.models import Reserve


class UpdateReserveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reserve
        exclude = (
            "user", "car", "reserve_status", "updated_at",
            "date_of_change_status", "created_at",
        )
