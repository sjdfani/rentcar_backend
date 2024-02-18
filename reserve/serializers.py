from rest_framework import serializers
from .models import Reserve, ReserveStatus
from car.models import Car, RentalTerms
from car.serializers import CarSerializer
from users.serializers import UserSerializer
from wallet.models import Deposit, Wallet
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
    end_rent_date = serializers.DateField()
    with_insurance = serializers.BooleanField()

    def validate(self, attrs):
        start_date = attrs.get('start_rent_date')
        end_date = attrs.get('end_rent_date')
        if start_date and end_date:
            if end_date < start_date:
                raise serializers.ValidationError(
                    "End date cannot be before start date.")
            difference = end_date - start_date
            attrs['days_difference'] = difference.days
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        obj = BasicPaymentInformation.objects.order_by("-pk").first()
        rental_terms = RentalTerms.objects.get(
            car__id=validated_data["car"].id)
        with_insurance = self.validated_data["with_insurance"]
        insurance_price = 0
        if with_insurance:
            insurance_price = (obj.insurance_percentage/100) * \
                rental_terms.car_object.car_value
        value_added = (obj.value_added_percentage/100) * \
            (rental_terms.price_each_day * rental_terms.min_days_to_rent)
        return Reserve.objects.create(
            user=user,
            car=validated_data["car"],
            start_rent_date=validated_data["start_rent_date"],
            end_rent_date=validated_data["end_rent_date"],
            days_to_rent=validated_data["days_difference"],
            price_each_day=rental_terms.price_each_day,
            value_added=value_added,
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
        user = self.context["request"].user
        obj = BasicPaymentInformation.objects.order_by("-pk").first()
        reserve = Reserve.objects.get(pk=self.validated_data["reserve"])
        reserve.payment_process(
            tracking_payment=self.validated_data["tracking_payment"],
            bank_name=self.validated_data["bank_name"],
        )
        Deposit.objects.create(
            reserve=reserve,
            rent_price=reserve.price_each_day * reserve.min_days_to_rent,
            car_value=reserve.car.car_value,
            company_percentage=obj.company_percentage,
            value_added_percentage=obj.value_added_percentage,
            insurance_percentage=obj.insurance_percentage,
        )
        total_price_rent = reserve.min_days_to_rent * reserve.price_each_day
        user_share_price = total_price_rent - \
            (total_price_rent * obj.company_percentage)
        wallet = Wallet.objects.get(user=user)
        wallet.deposit_process(user_share_price)


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
