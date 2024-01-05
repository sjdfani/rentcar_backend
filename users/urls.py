from django.urls import path
from .views import (
    Login, Register, ChangePassword, GetUsersList, RetrieveUpdateDestroyUsers,
    RetrieveUpdateUser, ForgotPassword, VerifyForgotPassword, ConfirmForgotPassword,
)

app_name = "users"

urlpatterns = [
    path("login/", Login.as_view(), name='login'),
    path("register/", Register.as_view(), name='register'),
    path("change-password/", ChangePassword.as_view(), name='change-password'),
    path("list/", GetUsersList.as_view(), name="users-list"),
    path("list/<int:pk>/", RetrieveUpdateDestroyUsers.as_view(),
         name="retrieve-update-destroy-user"),
    path("update/<int:pk>/", RetrieveUpdateUser.as_view(),
         name="retrieve-update-user"),
    path("forgot-password/", ForgotPassword.as_view(), name="forgot-password"),
    path("verify-forgot-password/", VerifyForgotPassword.as_view(),
         name="verify-forgot-password"),
    path("confirm-forgot-password/", ConfirmForgotPassword.as_view(),
         name="confirm-forgot-password"),
]
