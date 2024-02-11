from rest_framework import serializers
from .models import (
    Manufacturer, CarModel, Category, CarOptions, CarYear, CarTemplate,
    TechnicalSpecifications, Car, Color, City, CarImage, Comment, RentalTerms,
)
from users.serializers import UserSerializer
from city.serializers import CitySerializer


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = "__all__"

    def validate_name(self, value):
        if Manufacturer.objects.filter(name=value).exists():
            raise serializers.ValidationError("This manufacturer is exists.")
        return value


class CarModelSerializer(serializers.ModelSerializer):
    manufacturers = ManufacturerSerializer(read_only=True)

    class Meta:
        model = CarModel
        fields = "__all__"


class CreateCarModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarModel
        fields = "__all__"

    def validate_name(self, value):
        if CarModel.objects.filter(name=value).exists():
            raise serializers.ValidationError("This car model is exists.")
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("This category is exists.")
        return value


class CarOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarOptions
        fields = "__all__"

    def validate_name(self, value):
        if CarOptions.objects.filter(name=value).exists():
            raise serializers.ValidationError("This Car option is exists.")
        return value


class CarYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarYear
        fields = "__all__"


class TechnicalSpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalSpecifications
        fields = "__all__"


class CarTemplateSerializer(serializers.ModelSerializer):
    Technical_specifications = TechnicalSpecificationsSerializer()

    class Meta:
        model = CarTemplate
        fields = "__all__"


class UpdateCarTemplateSerializer(serializers.ModelSerializer):
    Technical_specifications = TechnicalSpecificationsSerializer()

    class Meta:
        model = CarTemplate
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.model = validated_data.get("model", instance.model)
        technical_specifications = validated_data.get(
            "Technical_specifications", None)
        if technical_specifications:
            obj = TechnicalSpecifications.objects.create(
                **technical_specifications)
            instance.Technical_specifications = obj
        category = validated_data.get(category, None)
        if category:
            instance.category.set(category)
        instance.save()


class CreateCarTemplateSerializer(serializers.Serializer):
    model = serializers.PrimaryKeyRelatedField(
        queryset=CarModel.objects.all()
    )
    body_style = serializers.CharField()
    gearbox_type = serializers.CharField()
    cylinder = serializers.IntegerField()
    capacity = serializers.IntegerField()
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True
    )

    def validate_model(self, value):
        if CarTemplate.objects.filter(model=value).exists():
            raise serializers.ValidationError("This car template is exists.")
        return value

    def validate_cylinder(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "You should enter positive number.")
        return value

    def validate_capacity(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "You should enter positive number.")
        return value

    def create(self, validated_data):
        ts_object = TechnicalSpecifications.objects.create(
            body_style=validated_data["body_style"],
            gearbox_type=validated_data["gearbox_type"],
            cylinder=validated_data["cylinder"],
            capacity=validated_data["capacity"],
        )
        car_template = CarTemplate.objects.create(
            model=validated_data["model"],
            Technical_specifications=ts_object,
        )
        car_template.category.set(validated_data["category"])
        return car_template


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"


class CarSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    car_template = CarTemplateSerializer(read_only=True)
    city = CitySerializer(read_only=True)
    color = ColorSerializer(read_only=True)
    year = CarYearSerializer(read_only=True)
    car_option = CarOptionsSerializer(many=True)

    class Meta:
        model = Car
        fields = "__all__"


class UpdateCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = (
            "color", "city", "year", "description",
            "car_value", "mileage", "is_out_of_service",
        )


class CreateCarSerializer(serializers.Serializer):
    model = serializers.PrimaryKeyRelatedField(
        queryset=CarModel.objects.all()
    )
    year = serializers.PrimaryKeyRelatedField(
        queryset=CarYear.objects.filter(status=True)
    )
    color = serializers.PrimaryKeyRelatedField(
        queryset=Color.objects.filter(status=True)
    )
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.filter(status=True)
    )
    plate = serializers.CharField()
    car_value = serializers.IntegerField()
    description = serializers.CharField(required=False)
    mileage = serializers.CharField()
    car_option = serializers.PrimaryKeyRelatedField(
        queryset=CarOptions.objects.all(), many=True
    )

    def validate_plate(self, value):
        if Car.objects.filter(plate=value).exists():
            raise serializers.ValidationError("This plate is exists in db.")
        return value

    def create(self, validated_data):
        request = self.context["request"]
        car_options = validated_data.pop("car_option")
        model = validated_data.pop("model")
        car_template = CarTemplate.objects.get(model=model)
        obj = Car.objects.create(
            owner=request.user,
            car_template=car_template,
            **validated_data
        )
        obj.car_option.set(car_options)
        obj.save()
        status = False
        for _, image in request.FILES.items():
            CarImage.objects.create(car_object=obj, image=image)
            status = True
        obj.change_has_media(
            True) if status is True else obj.change_has_media(False)
        return obj


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CreateCommentSerializer(serializers.Serializer):
    car_object = serializers.PrimaryKeyRelatedField(
        queryset=Car.objects.all()
    )
    text = serializers.CharField()

    def create(self, validated_data):
        user = self.context["request"].user
        return Comment.objects.create(
            user=user,
            car_object=validated_data["car_object"],
            text=validated_data["text"]
        )


class CreateRentalTermsSerializer(serializers.Serializer):
    car_object = serializers.PrimaryKeyRelatedField(
        queryset=Car.objects.all()
    )
    cancellation_policy = serializers.CharField()
    min_days_to_rent = serializers.IntegerField()
    max_km_per_day = serializers.IntegerField()
    extra_km_price = serializers.IntegerField()
    extra_hour_price = serializers.IntegerField()
    price_each_day = serializers.IntegerField()
    deliver_at_renters_place = serializers.BooleanField()
    with_driver = serializers.BooleanField()
    without_driver = serializers.BooleanField()

    def validate_car_object(self, value):
        user = self.context["request"].user
        if not Car.objects.filter(owner=user, pk=value.pk).exists():
            raise serializers.ValidationError("This car is not exists.")
        return value

    def create(self, validated_data):
        create_process = super().create(validated_data)
        car_object = validated_data["car_object"]
        car_object.change_has_complete_info(True)
        return create_process


class UpdateRentalTermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalTerms
        exclude = ("car_object",)
