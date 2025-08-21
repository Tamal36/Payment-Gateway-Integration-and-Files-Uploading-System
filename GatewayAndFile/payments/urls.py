from django.urls import path
from .views import *

urlpatterns = [
    path('register/',           register_user, name='register-user'),
    path('profile/',            get_user_profile, name='get-user-profile'),
    path('initiate-payment/',   initiate_payment, name='initiate-payment'),
    path('payment/success/',    payment_success, name='payment-success'),
    path('payment/failed/',     payment_failed, name='payment-failed'),
    path('payment/cancelled/',  payment_cancelled, name='payment-cancelled'),
    path('login-view/',         login_view, name='login-view'), # UI
    path('transactions-view/',  transaction_history_view, name='transaction-history-view'), # UI
    path('payment/transactions/', get_user_transactions, name='get-user-transaction'),
]
