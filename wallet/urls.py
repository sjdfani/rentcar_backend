from django.urls import path
from . import views

app_name = "wallet"

urlpatterns = [
    path("get/", views.GetWalletByUser.as_view(), name="GetWalletByUser"),

    path("withdrawal/request/", views.WithdrawalRequest.as_view(),
         name="WithdrawalRequest"),
    path("withdrawal/payment/", views.DoneWithdrawal.as_view(),
         name="DoneWithdrawal"),
    path("withdrawal/list/", views.WithdrawalList.as_view(),
         name="WithdrawalList"),

    path("deposit/owner/list/", views.DepositListByOwner.as_view(),
         name="WithdrawalList"),
    path("deposit/user/list/", views.DepositListByUser.as_view(),
         name="WithdrawalList"),
]
