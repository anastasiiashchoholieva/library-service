from django.urls import path

from .views import PaymentSuccessView, PaymentCancelView

urlpatterns = [
    path("success/", PaymentSuccessView.as_view(), name="success-payment"),
    path("cancel/", PaymentCancelView.as_view(), name="cancel-payment"),
]

app_name = "payments"
