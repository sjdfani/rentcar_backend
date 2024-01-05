from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import CustomUser, EmailCode
from .utils import str_generator, get_user_messages
from .tasks import send_email


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        exclude = ("password",)


class UpdateUserSerializer(serializers.ModelSerializer):

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                get_user_messages("email_exists"))
        return value

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                get_user_messages("username_exists"))
        return value

    class Meta:
        model = CustomUser
        fields = ("email", "username", "first_name", "last_name", "photo")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                get_user_messages("email_not_exists"))
        return value


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=20)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise ValidationError(
                {"email": get_user_messages("email_exists")})
        if CustomUser.objects.filter(username=attrs['username']).exists():
            raise ValidationError(
                {"username": get_user_messages("username_exists")})
        if attrs['password1'] != attrs['password2']:
            raise ValidationError(
                {"passwords": get_user_messages("equal_passwords")})
        return attrs

    def send_verify_code(self, user: CustomUser):
        code = str_generator(5, True)
        obj = EmailCode.objects.get_or_create(user=user)[0]
        obj.set_unique_id_and_code(code)
        # send_email.delay(code, user.email)
        print(f"Verify code: {code}")

    def create(self, validated_data):
        validated_data.pop("password1")
        password = validated_data.pop("password2")
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.disable_user()
        self.send_verify_code(user)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        user = self.context["request"].user
        if not user.check_password(attrs["current_password"]):
            raise ValidationError(
                {"current-password": get_user_messages("wrong_password")})
        if attrs["new_password"] != attrs["confirm_password"]:
            raise ValidationError(
                {"passwords": get_user_messages("equal_passwords")})
        return attrs

    def change_password(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return {"message": "Your password changed"}


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value):
            raise serializers.ValidationError(
                get_user_messages("email_not_exists"))
        return value

    def generate_code_and_send_email(self, user):
        code = str_generator(5, True)
        obj = EmailCode.objects.get_or_create(user=user)[0]
        obj.set_unique_id_and_code(code)
        # send_email.delay(code, user.email)
        print(f"code: {code}")
        return obj.unique_id

    def save(self):
        email = self.validated_data["email"]
        user = CustomUser.objects.get(email=email)
        return self.generate_code_and_send_email(user)


class VerifyForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    unique_id = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        if not EmailCode.objects.filter(unique_id=attrs["unique_id"], status=True).exists():
            raise ValidationError(
                {"forgot-password": get_user_messages("unique_id_not_found")})
        return attrs

    def verify_code(self, user, unique_id: str, code: str):
        obj = EmailCode.objects.filter(
            user=user, unique_id=unique_id, status=True).first()
        if obj:
            if code == obj.code:
                return (True, {"message": get_user_messages("correct_code")})
            else:
                return (False, {"message": get_user_messages("invalid_code")})
        else:
            return (False, {"message": get_user_messages("expire_code")})

    def verify_forgot_password_process(self):
        code = self.validated_data["code"]
        unique_id = self.validated_data["unique_id"]
        user = CustomUser.objects.get(email=self.validated_data["email"])
        return self.verify_code(user, unique_id, code)


class ConfirmForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    unique_id = serializers.CharField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if not CustomUser.objects.filter(email=attrs["email"]).exists():
            raise ValidationError(
                {"email": get_user_messages("email_not_exists")})
        if not EmailCode.objects.filter(unique_id=attrs["unique_id"]).exists():
            raise ValidationError(
                {"unique_id": get_user_messages("unique_id_not_found")})
        if attrs['password1'] != attrs['password2']:
            raise ValidationError(
                {"passwords": get_user_messages("equal_passwords")})
        return attrs

    def set_new_password(self, user, unique_id: str, password: str):
        obj = EmailCode.objects.filter(
            user=user, unique_id=unique_id, status=True).first()
        if obj:
            user.set_password(password)
            user.save()
            return (True, {"message": get_user_messages("successful_change_password")})
        else:
            return (False, {"message": get_user_messages("expire_code")})

    def confirm_password_process(self):
        password = self.validated_data["password1"]
        unique_id = self.validated_data["unique_id"]
        user = CustomUser.objects.get(email=self.validated_data["email"])
        return self.set_new_password(user, unique_id, password)
