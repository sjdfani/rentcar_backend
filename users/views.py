from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView,
)
from .serializers import (
    LoginSerializer, UpdateUserSerializer, UserSerializer, RegisterSerializer,
    ForgotPasswordSerializer, VerifyForgotPasswordSerializer,
    ConfirmForgetPasswordSerializer, ChangePasswordSerializer,
)
from .models import CustomUser
from .utils import get_tokens_for_user
from .permissions import IsSuperuser
from car.models import Comment, Car, CarStatus
from car.serializers import CommentSerializer, CarSerializer


class Login(APIView):
    def post(self, request):
        serializer = LoginSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = CustomUser.objects.get(email=email)
        if user.check_password(password):
            user.update_last_login()
            message = {
                "user": UserSerializer(user).data,
                "tokens": get_tokens_for_user(user),
            }
            return Response(message, status=status.HTTP_200_OK)
        else:
            message = {"message": "Your email or password is incorrect."}
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)


class Register(APIView):
    def post(self, request):
        serializer = RegisterSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email = serializer.validated_data.get('email')
        user = CustomUser.objects.get(email=email)
        user.update_last_login()
        message = {
            "user": UserSerializer(user).data,
            "tokens": get_tokens_for_user(user),
        }
        return Response(message, status=status.HTTP_201_CREATED)


class ChangePassword(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        response = serializer.change_password()
        return Response(response, status=status.HTTP_200_OK)


class GetUsersList(ListAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()


class RetrieveUpdateDestroyUsers(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsSuperuser,)
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()


class RetrieveUpdateUser(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return CustomUser.objects.filter(email=self.request.user.email)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserSerializer
        return UpdateUserSerializer


class ForgotPassword(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        unique_id = serializer.save()
        return Response({"code": unique_id}, status=status.HTTP_200_OK)


class VerifyForgotPassword(APIView):
    def post(self, request):
        serializer = VerifyForgotPasswordSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        state, message = serializer.verify_forgot_password_process()
        if state:
            return Response(message, status=status.HTTP_200_OK)
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class ConfirmForgotPassword(APIView):
    def post(self, request):
        serializer = ConfirmForgetPasswordSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        state, message = serializer.confirm_password_process()
        if state:
            return Response(message, status=status.HTTP_200_OK)
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class UserDetails(APIView):
    def get(self, request):
        pk = self.kwargs.get("pk", None)
        user_obj = CustomUser.objects.filter(pk=pk)
        if user_obj.exists():
            user = user_obj.first()
            comment_objs = Comment.objects.filter(user=user)
            car_objs = Car.objects.filter(
                owner=user, status=CarStatus.ACCEPTED)
            message = {
                "user_info": UserSerializer(user).data,
                "comments": CommentSerializer(comment_objs, many=True).data,
                "cars": CarSerializer(car_objs, many=True).data,
            }
            return Response(message, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
