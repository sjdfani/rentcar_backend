from django.urls import path
import views

app_name = "wallet"

urlpatterns = [
    path("get/", views.GetWalletByUser.as_view(), name="GetWalletByUser"),
    path("withdrawal/request/", views.WithdrawalRequest.as_view(),
         name="WithdrawalRequest"),
    path("withdrawal/payment/", views.DoneWithdrawal.as_view(),
         name="DoneWithdrawal"),
]
