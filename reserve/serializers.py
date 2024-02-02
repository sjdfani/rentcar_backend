from rest_framework import serializers
from .models import Reserve, ReserveStatus
from car.models import Car, RentalTerms
from car.serializers import CarSerializer
from users.serializers import UserSerializer
from wallet.models import Deposit
from panel.models import BasicPaymentInformation


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
    with_insurance = serializers.BooleanField()

    def create(self, validated_data):
        user = self.context["request"].user
        rental_terms = RentalTerms.objects.get(pk=validated_data["car"].pk)
        with_insurance = self.validated_data["with_insurance"]
        insurance_price = 0
        if with_insurance:
            obj = BasicPaymentInformation.objects.order_by("-pk").first()
            insurance_price = obj.insurance_percentage*rental_terms.car_object.car_value
            with_insurance = True
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


class ChangeReserveStatusSerializer(serializers.Serializer):
    reserve = serializers.IntegerField()
    status = serializers.CharField()

    def validate_reserve(self, value):
        user = self.context["request"].user
        if value < 0:
            raise serializers.ValidationError("Please enter positive value")
        if not Reserve.objects.filter(pk=value, car__owner=user).exists():
            raise serializers.ValidationError(
                "Please enter your car reservation id.")
        return value

    def validate_status(self, value):
        if value not in tuple(choice.value for choice in ReserveStatus):
            raise serializers.ValidationError("Please choose right status.")
        return value

    def save(self, **kwargs):
        reserve = self.validated_data["reserve"]
        status = self.validated_data["status"]
        if status == ReserveStatus.ACCEPTED:
            reserve.change_status(ReserveStatus.ACCEPTED)
        elif status == ReserveStatus.PENDING:
            reserve.change_status(ReserveStatus.PENDING)
        elif status == ReserveStatus.REJECTED:
            reserve.change_status(ReserveStatus.REJECTED)


class PaymentReserveSerializer(serializers.Serializer):
    reserve = serializers.IntegerField()
    tracking_payment = serializers.CharField()
    bank_name = serializers.CharField()

    def validate_reserve(self, value):
        user = self.context["request"].user
        if value < 0:
            raise serializers.ValidationError("Please enter positive value.")
        if not Reserve.objects.filter(
                pk=value, user=user, status=ReserveStatus.ACCEPTED).exists():
            raise serializers.ValidationError(
                "Please enter your car reservation id.")
        return value

    def save(self, **kwargs):
        # fix payment (added_value, insurance_price, price_each_day*min_days_to_rent)
        # call Deposit model and create a deposit object with (price_each_day * min_days_to_rent)
        reserve = Reserve.objects.get(pk=self.validated_data["reserve"])
        reserve.payment_process(
            tracking_payment=self.validated_data["tracking_payment"],
            bank_name=self.validated_data["bank_name"],
        )


class FinishRentTimeSerializer(serializers.Serializer):
    reserve = serializers.IntegerField()

    def validate_reserve(self, value):
        user = self.context["request"].user
        if value < 0:
            raise serializers.ValidationError("Please enter positive value")
        if not Reserve.objects.filter(pk=value, car__owner=user).exists():
            raise serializers.ValidationError(
                "Please enter your car reservation id.")
        return value

    def save(self, **kwargs):
        reserve = Reserve.objects.get(self.validated_data["reserve"])
        car = Car.objects.get(pk=reserve.car.pk)
        car.is_available = True
        car.save()
