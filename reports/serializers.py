from datetime import datetime
from rest_framework import serializers
from car.models import Car, CarStatus
from reserve.models import Reserve
from users.models import CustomUser


class ReportUsersWithAcceptedCarSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)

    def get_data(self):
        start_date = self.validated_data.get("start_date", None)
        end_date = self.validated_data.get("end_date", None)
        if start_date and end_date:
            user_count = Car.objects.filter(
                status=CarStatus.ACCEPTED,
                created_at__range=(start_date, end_date)
            ).values('owner').distinct().count()
        else:
            user_count = Car.objects.filter(
                status=CarStatus.ACCEPTED).values('owner').distinct().count()
        message = {
            "user_count": user_count,
        }
        return message


class ReportUsersSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)

    def get_data(self):
        start_date = self.validated_data.get("start_date", None)
        end_date = self.validated_data.get("end_date", None)
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            user_count = CustomUser.objects.filter(
                created_at__range=(start_date, end_date)).count()
        else:
            user_count = CustomUser.objects.all().count()
        message = {
            "user_count": user_count,
        }
        return message


class ReportUsersAtLeastReserveCarSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)

    def get_data(self):
        start_date = self.validated_data.get("start_date", None)
        end_date = self.validated_data.get("end_date", None)
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            user_count = Reserve.objects.filter(
                created_at__range=(start_date, end_date)
            ).values('user').distinct().count()
        else:
            user_count = Reserve.objects.values('user').distinct().count()
        message = {
            "user_count": user_count,
        }
        return message
