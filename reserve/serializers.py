from rest_framework import serializers
from .models import Reserve
from car.models import Car, RentalTerms
from car.serializers import CarSerializer
from users.serializers import UserSerializer


class ReserveSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    car = CarSerializer()

    class Meta:
        model = Reserve
        fields = "__all__"


class CreateReserveSerializer(serializers.Serializer):
    car = serializers.PrimaryKeyRelatedField(
        queryset=Car.objects.filter(is_available=True, is_out_of_service=False)
    )
    start_rent_date = serializers.DateField()
    value_added = serializers.IntegerField()
    insurance_price = serializers.IntegerField(required=False)

    def validate_value_added(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "You can't enter negative price.")
        return value

    def validate_insurance_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "You can't enter negative price.")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        rental_terms = RentalTerms.objects.get(pk=validated_data["car"].pk)
        with_insurance = True
        insurance_price = validated_data.get("insurance_price", None)
        if not insurance_price:
            insurance_price = 0
            with_insurance = False
        return Reserve.objects.create(
            user=user,
            car=validated_data["car"],
            start_rent_date=validated_data["start_rent_date"],
            min_days_to_rent=rental_terms.min_days_to_rent,
            price_each_day=rental_terms.price_each_day,
            value_added=validated_data["value_added"],
            with_insurance=with_insurance,
            insurance_price=insurance_price,
        )
