from django.urls import path
from .views import PaymentChannelListView, CreatePaymentView, PaymenkuWebhookView

urlpatterns = [
    path('payments/channels/', PaymentChannelListView.as_view(), name='payment-channels'),
    path('payments/create/', CreatePaymentView.as_view(), name='payment-create'),
    path('payments/webhook/', PaymenkuWebhookView.as_view(), name='payment-webhook'),
]