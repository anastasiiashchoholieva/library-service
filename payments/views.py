from django.http import HttpResponse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from payments.models import Payment
from payments.serializers import PaymentSerializer


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.select_related()
    serializer_class = PaymentSerializer


class PaymentSuccessView(APIView):
    def get(self, request, session_id):
        payment = Payment.objects.filter(session_id=session_id).first()
        if payment and payment.status != Payment.PaymentStatus.PAID:
            payment.status = Payment.PaymentStatus.PAID
            payment.save()
            return Response("Payment was successful")
        return Response("Payment not found")


class PaymentCancelView(APIView):
    def get(self, request, session_id):
        payment = Payment.objects.filter(session_id=session_id).first()
        if payment and payment.status != Payment.PaymentStatus.PAID:
            payment.status = Payment.PaymentStatus.CANCELLED
            payment.save()
            return Response("Payment can be paid a bit later")
