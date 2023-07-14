from django.urls import path

from .views import PaymentSuccessView, PaymentCancelView, PaymentListView

urlpatterns = [
    path("payments/", PaymentListView.as_view(), name="payment-list"),
    path("payments/<str:session_id>/success/", PaymentSuccessView.as_view(), name="payment-success"),
    path("payments/<str:session_id>/cancel/", PaymentCancelView.as_view(), name="payment-cancel"),
]

app_name = "payments"
