from rest_framework import serializers
from .models import City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"

    def validate_name(self, value):
        if City.objects.filter(name=value).exists():
            raise serializers.ValidationError("This city is exists.")
        return value
